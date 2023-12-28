from yahtzee.scores import categories, get_score_for_category
import sqlite3
from strategies.Strategy import Strategy


class ProbStrategy(Strategy):
    def __init__(self):
        conn = sqlite3.connect('prob_db/prob_db.db')
        self.cursor = conn.cursor()

    def get_ranked_keep_numbers(self, roll, available_categories, _):
        key = "".join([str(d) for d in roll])
        query = f'''
        SELECT roll, keep, l1.strat, l1.ev_frac as ev, ev_score
        FROM level1 as l1
        WHERE l1.roll = (?) and l1.strat = (?)
        ORDER BY ev, ev_score DESC
        LIMIT 1
        '''
        
        possibilities = []
        for category in available_categories:
            self.cursor.execute(query, [key, category])
            results = self.cursor.fetchall()
            for row in results:
                possibilities.append((row[1], row[2], round(row[3], 2), round(row[4], 2)))
        possibilities.sort(key=lambda x: (x[2], x[3]), reverse=True)
        return [int(d) for d in possibilities[0][0]]

    def get_keep_number_choice(self, roll, available_categories, _):
        return self.get_ranked_keep_numbers(roll, available_categories, _)[0]

    def get_ranked_category_choices(self, available_categories, roll, scoreboard):
        fracs_and_scores = []
        for category in available_categories:
            (score, _)  = get_score_for_category(category, roll, scoreboard)
            max = categories[category]["max"]
            fracs_and_scores.append((score/max, score, category))
        fracs_and_scores.sort(reverse=True)
        return fracs_and_scores[0][2]
    
    def get_category_choice(self, available_categories, roll, scoreboard):
        return self.get_ranked_category_choices(available_categories, roll, scoreboard)[0]