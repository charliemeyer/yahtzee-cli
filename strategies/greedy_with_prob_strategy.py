from strategies.scores import strategies, get_score_for_category
import sqlite3
conn = sqlite3.connect('strategies/prob_db.db')
cursor = conn.cursor()

def get_keep_numbers(roll, available_categories):
    key = "".join([str(d) for d in roll])
    query = '''
    SELECT roll, keep, strat, ev_frac, ev_score
    FROM level1
    WHERE roll = (?) and strat = (?)
    ORDER BY ev_frac DESC, ev_score DESC
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
    best_category = available_categories[0]
    best_score = get_score_for_category(available_categories[0], roll, scoreboard)
    for category in available_categories:
        score = get_score_for_category(category, roll, scoreboard)
        if score > best_score:
            best_score = score
            best_category = category
    return best_category