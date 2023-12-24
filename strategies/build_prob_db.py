import sqlite3
from scores import strategies, get_score_for_category
from dice_edit_distance import dice_edit_distance

all_rolls = {"11111"}
for i in range(1,7):
    for j in range(1,7):
        for k in range(1,7):
            for l in range(1,7):
                for m in range(1,7):
                    roll = "".join([str(n) for n in sorted([i, j, k, l, m])])
                    all_rolls.add(roll)

conn = sqlite3.connect('prob_db.db')
cursor = conn.cursor()

#
# all rolls table
#
cursor.execute('''CREATE TABLE IF NOT EXISTS rolls (roll TEXT)''')
for row in list(all_rolls):
    cursor.execute("INSERT INTO rolls (roll) VALUES (?)", [row])
conn.commit()


#
# roll transitions table
#
cursor.execute('''CREATE TABLE IF NOT EXISTS roll_transitions (roll1 TEXT, roll2 TEXT, prob FLOAT)''')

data_to_write = []
for roll1 in all_rolls:
    for roll2 in all_rolls:
        data_to_write.append((roll1, roll2, dice_edit_distance(roll1, roll2)))

for row in data_to_write:
    cursor.execute("INSERT INTO roll_transitions (roll1, roll2, prob) VALUES (?, ?, ?)", row)

conn.commit()

#
# level 0 scores table
#
cursor.execute('''CREATE TABLE IF NOT EXISTS level0 (roll TEXT, strat TEXT, ev FLOAT)''')
data_to_write = []

for roll in all_rolls:
    for strat in strategies:
        (score, _) = get_score_for_category(strat, [int(d) for d in roll], {"num_yahtzees": 0})
        data_to_write.append((roll, strat, score))

for row in data_to_write:
    cursor.execute("INSERT INTO level0 (roll, strat, ev) VALUES (?, ?, ?)", row)

conn.commit()


#
# level 1 transitions table
#

cursor.execute('''CREATE TABLE IF NOT EXISTS level1 (roll TEXT, strat TEXT, ev FLOAT)''')

query = '''
SELECT r.roll, rs.strat, AVG(rs.ev * rt.prob) AS avg_score_prob
FROM rolls r
JOIN roll_transitions rt ON r.roll = rt.roll1
JOIN level0 rs ON rt.roll2 = rs.roll
GROUP BY r.roll, rs.strat
'''


cursor.execute(query)
rows = cursor.fetchall()
for row in rows:
    cursor.execute("INSERT INTO level1 (roll, strat, ev) VALUES (?, ?, ?)", row)

conn.commit()
conn.close()