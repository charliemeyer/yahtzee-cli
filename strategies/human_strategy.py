import sqlite3

conn = sqlite3.connect('strategies/prob_db.db')
cursor = conn.cursor()

def get_keep_numbers(roll, available_categories):
    good_keep_numbers = False
    keep_numbers = []
    key = "".join([str(d) for d in roll])
    query = '''
    SELECT r.roll, rt.keep, rs.strat, SUM(rt.prob * rs.ev_frac) as ev_frac, SUM(rt.prob * rs.ev) as ev_score
    FROM rolls r
    JOIN roll_transitions rt ON r.roll = rt.roll1
    JOIN level0 rs ON rt.roll2 = rs.roll
    WHERE r.roll = (?) and rs.strat = (?)
    GROUP BY rs.strat, rt.keep
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
    for p in possibilities:
        print(p)
    while not good_keep_numbers:
        keep_choice = input("what numbers do you want to keep? (\"all\" to keep all, \"none\" to keep none)\n")
        if keep_choice == "all":
            return roll
        try:
            keep_numbers = [] if keep_choice == "none" else [int(n) for n in keep_choice]
            good_keep_numbers = True
        except:
            print("invalid keep numbers")
            continue
        if keep_choice == "all":
            break
        for n in keep_numbers:
            if n not in roll:
                print("invalid keep number")
                good_keep_numbers = False
                break
    return keep_numbers


def get_category_choice(available_categories, _roll, _scoreboard):
    chosen_category = input("what category do you want to use?\n")
    while chosen_category not in available_categories:
        print("invalid category")
        chosen_category = input("what category do you want to use?\n")
        continue
    return chosen_category