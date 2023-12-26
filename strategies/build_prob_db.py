import sqlite3
from scores import strategies, get_score_for_category
from dice_edit_distance import dice_edit_distance
from scores import strategies
import itertools

def get_all_subsets(lst):
    subsets = []
    for i in range(len(lst) + 1):
        for subset in itertools.combinations(lst, i):
            subsets.append("".join(subset))
    return subsets

def rolls_to_set(rolls):
    return set(["".join(sorted(r)) for r in rolls])

single_rolls = [[str(d)] for d in range(1,7)]
double_rolls = [[str(d)] + roll for d in range (1,7) for roll in single_rolls]
triple_rolls = [[str(d)] + roll for d in range (1,7) for roll in double_rolls]
quad_rolls = [[str(d)] + roll for d in range (1,7) for roll in triple_rolls]
five_rolls = [[str(d)] + roll for d in range (1,7) for roll in quad_rolls]
all_rolls_set = set(["".join(sorted(r)) for r in five_rolls])

rolls_list = [rolls_to_set(rolls) for rolls in [[[]], single_rolls, double_rolls, triple_rolls, quad_rolls, five_rolls]]

conn = sqlite3.connect('prob_db.db')
cursor = conn.cursor()

#
# all rolls table
#
cursor.execute('''CREATE TABLE IF NOT EXISTS rolls (roll TEXT)''')
for row in list(all_rolls_set):
    cursor.execute("INSERT INTO rolls (roll) VALUES (?)", [row])
conn.commit()

print("all rolls table done")

#
# roll transitions table
#
cursor.execute('''CREATE TABLE IF NOT EXISTS roll_transitions (roll1 TEXT, keep TEXT, roll2 TEXT, prob FLOAT)''')

data_to_write = []
for roll1 in all_rolls_set:
    
    for keep in set(["".join(sorted(s)) for s in get_all_subsets(roll1)]):
        new_rolls = []
        for rest_roll in rolls_list[5 - len(keep)]:
            roll2 = "".join([str(d) for d in sorted(keep + rest_roll)])
            keep_key = "".join([str(d) for d in sorted(keep)])
            data_to_write.append((roll1, keep_key, roll2, dice_edit_distance(keep_key, roll2)))

for row in data_to_write:
    cursor.execute("INSERT INTO roll_transitions (roll1, keep, roll2, prob) VALUES (?, ?, ?, ?)", row)

conn.commit()

print("roll transitions table done")

#
# level 0 scores table
#
cursor.execute('''CREATE TABLE IF NOT EXISTS level0 (roll TEXT, strat TEXT, ev FLOAT, ev_frac FLOAT)''')
data_to_write = []

for roll in all_rolls_set:
    for strat in strategies:
        (score, _) = get_score_for_category(strat, [int(d) for d in roll], {"num_yahtzees": 0})
        data_to_write.append((roll, strat, score / strategies[strat]["max"], score))

for row in data_to_write:
    cursor.execute("INSERT INTO level0 (roll, strat, ev_frac, ev) VALUES (?, ?, ?, ?)", row)

conn.commit()

print("level 0 scores table done")

#
# level 1 transitions table
#

cursor.execute('''CREATE TABLE IF NOT EXISTS level1 (roll TEXT, keep TEXT, strat TEXT, ev_frac FLOAT, ev_score FLOAT)''')

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

print("queries to do total: ", len(all_rolls_set) * len(strategies))

count = 0
for strat in strategies:
    for roll in all_rolls_set:
        cursor.execute(query, [roll, strat])
        results = cursor.fetchall()
        for row in results:
            cursor.execute("INSERT INTO level1 (roll, keep, strat, ev_frac, ev_score) VALUES (?, ?, ?, ?, ?)", [roll, row[1], strat, row[3], row[4]])
        count += 1
        if count % 100 == 0:
            print(count, "done")


conn.commit()

conn.close()