import sqlite3

conn = sqlite3.connect('strategies/prob_db.db')
cursor = conn.cursor()

def get_keep_numbers(roll, available_categories, rolls_left):
    good_keep_numbers = False
    keep_numbers = []
    key = "".join([str(d) for d in roll])
    query = f'''
    SELECT roll, keep, SUM(l1.ev_frac / d.ev_frac) as ev, AVG(ev_score) as ev_score
    FROM level1 as l1
    JOIN difficulty d on d.strat = l1.strat
    WHERE l1.roll = (?) and l1.strat in {"(" + ",".join([f'"{cat}"' for cat in available_categories]) + ")"}
    GROUP BY keep
    ORDER BY ev, ev_score DESC
    '''

    possibilities = []
    cursor.execute(query, [key, ])
    results = cursor.fetchall()
    for row in results:
        possibilities.append((row[1], row[2], round(row[3], 2)))
    possibilities.sort(key=lambda x: (x[1], x[2]), reverse=True)
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