# 
# score all rolls against all strategies 13 * ~252 9360
# 
# 
# 
# 
# 
# 
# 
# 
# 
# desired: roll + expected value while maximizing for each strategy level 0, level 1, level 2, level 3
from scores import strategies, get_score_for_category
import sqlite3

all_rolls = {"11111"}
for i in range(1,7):
    for j in range(1,7):
        for k in range(1,7):
            for l in range(1,7):
                for m in range(1,7):
                    roll = "".join([str(n) for n in sorted([i, j, k, l, m])])
                    all_rolls.add(roll)


data_to_write = []  # Each tuple is a row

for roll in all_rolls:
    for strat in strategies:
        (score, _) = get_score_for_category(strat, [int(d) for d in roll], {"num_yahtzees": 0})
        data_to_write.append((roll, strat, score))

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('roll_scores.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table (if it doesn't already exist)
cursor.execute('''CREATE TABLE IF NOT EXISTS roll_scores (roll TEXT, strat_id TEXT, score INTEGER)''')

# Insert data into the table
for row in data_to_write:
    cursor.execute("INSERT INTO roll_scores (roll, strat_id, score) VALUES (?, ?, ?)", row)

# Commit the changes
conn.commit()

# Close the connection
conn.close()