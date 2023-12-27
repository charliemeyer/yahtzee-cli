from strategies.scores import strategies, get_score_for_category
import sqlite3
conn = sqlite3.connect('strategies/prob_db.db')
cursor = conn.cursor()

def get_keep_numbers(roll, available_categories, roll_num):
    key = "".join([str(d) for d in roll])
    table = "level1"
    query = f'''
    SELECT roll, keep, SUM(l1.ev_frac / d.ev_frac) as ev, AVG(ev_score) as ev_score
    FROM {table} as l1
    JOIN difficulty d on d.strat = l1.strat
    WHERE l1.roll = (?) and l1.strat in {"(" + ",".join([f'"{cat}"' for cat in available_categories]) + ")"}
    GROUP BY keep
    ORDER BY ev, ev_score DESC
    '''
    
    possibilities = []
    cursor.execute(query, [key])
    results = cursor.fetchall()
    for row in results:
        possibilities.append((row[1], row[2], round(row[3], 2)))
    possibilities.sort(key=lambda x: (x[1], x[2]), reverse=True)
    # print("roll was", roll, "keep", possibilities[0][0])
    return [int(d) for d in possibilities[0][0]]


def get_category_choice(available_categories, roll, scoreboard):
    fracs_and_scores = []
    for category in available_categories:
        (score, _)  = get_score_for_category(category, roll, scoreboard)
        max = strategies[category]["max"]
        fracs_and_scores.append((score/max, score, category, max))
    fracs_and_scores.sort(reverse=True)
    # if you have a bad roll, take the least important one
    if (fracs_and_scores[0][0] < .5):
        fracs_and_scores.sort(key=lambda x: 999 if x[1] <= 0 else x[3])
    # print("roll was", roll, "use strat", fracs_and_scores[0][2])
    return fracs_and_scores[0][2]