from yahtzee.scores import categories, get_score_for_category
import sqlite3
from strategies.Strategy import Strategy


class ProbWithDifficulty(Strategy):
    def __init__(self):
        conn = sqlite3.connect('prob_db/probs.db')
        self.cursor = conn.cursor()

    def get_ranked_keep_numbers(self, roll, available_categories, _roll_num):
        key = "".join([str(d) for d in roll])
        table = "level1"
        query = f'''
        SELECT roll, keep, SUM(l1.ev_frac / d.ev_frac) as ev, AVG(ev_score) as ev_score
        FROM {table} as l1
        JOIN difficulty d on d.category = l1.category
        WHERE l1.roll = (?) and l1.category in {"(" + ",".join([f'"{cat}"' for cat in available_categories]) + ")"}
        GROUP BY keep
        ORDER BY ev, ev_score DESC
        '''
        
        possibilities = []
        self.cursor.execute(query, [key])
        results = self.cursor.fetchall()
        for row in results:
            possibilities.append((row[1], row[2], round(row[3], 2)))
        possibilities.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return [([int(d) for d in p[0]], round(p[1], 2)) for p in possibilities][0:5]
    
    def get_keep_number_choice(self, roll, available_categories, roll_num):
        return self.get_ranked_keep_numbers(roll, available_categories, roll_num)[0][0]

    def get_ranked_category_choices(self, available_categories, roll, scoreboard):
        fracs_and_scores = []
        for category in available_categories:
            (score, _)  = get_score_for_category(category, roll, scoreboard)
            max = categories[category]["max"]
            fracs_and_scores.append((score/max, score, category, max))
        fracs_and_scores.sort(reverse=True)
        # if you have a bad roll, take the least important one
        if (fracs_and_scores[0][0] < .5):
            fracs_and_scores.sort(key=lambda x: 999 if x[1] <= 0 else x[3])
        return [fs[2] for fs in fracs_and_scores][0:5]

    def get_category_choice(self, available_categories, roll, scoreboard):
        return self.get_ranked_category_choices(available_categories, roll, scoreboard)[0]
