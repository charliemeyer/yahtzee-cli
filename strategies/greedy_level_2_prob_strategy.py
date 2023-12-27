from strategies.scores import strategies, get_score_for_category
import sqlite3
conn = sqlite3.connect('strategies/prob_db.db')
cursor = conn.cursor()

def get_keep_numbers(roll, available_categories, roll_num):
    key = "".join([str(d) for d in roll])
    table = ["level1", "level2"][roll_num]
    query = f'''
    SELECT roll, keep, l2.strat, l2.ev_frac as ev, ev_score
    FROM {table} as l2
    WHERE l2.roll = (?) and l2.strat = (?)
    ORDER BY ev, ev_score DESC
    LIMIT 1
    '''
    
    possibilities = []
    for category in available_categories:
        cursor.execute(query, [key, category])
        results = cursor.fetchall()
        for row in results:
            possibilities.append((row[1], row[2], round(row[3], 2), round(row[4], 2)))
    possibilities.sort(key=lambda x: (x[2], x[3]), reverse=True)
    return [int(d) for d in possibilities[0][0]]


def get_category_choice(available_categories, roll, scoreboard):
    fracs_and_scores = []
    for category in available_categories:
        (score, _)  = get_score_for_category(category, roll, scoreboard)
        max = strategies[category]["max"]
        fracs_and_scores.append((score/max, score, category))
    fracs_and_scores.sort(reverse=True)
    return fracs_and_scores[0][2]