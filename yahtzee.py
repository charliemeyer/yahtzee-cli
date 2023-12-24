import random
from scores import strategies, final_score
import sys

def roll(old_roll, keep_numbers):
    new_roll = []
    for i in range(5):
        if i < len(keep_numbers):
            # TODO: check if the keep number is actually legit
            new_roll.append(keep_numbers[i])
        else:
            new_roll.append(random.randint(1,6))
    return sorted(new_roll)

def get_keep_numbers(roll):
    good_keep_numbers = False
    keep_numbers = []
    while not good_keep_numbers:
        keep_choice = input("what numbers do you want to keep? (\"all\" to keep all, \"none\" to keep none)\n")
        if keep_choice == "all":
            return roll
        keep_numbers = [] if keep_choice == "none" else [int(n) for n in keep_choice]
        good_keep_numbers = True
        if keep_choice == "all":
            break
        for n in keep_numbers:
            if n not in user_roll:
                print("invalid keep number")
                good_keep_numbers = False
                break
    return keep_numbers

def show_scoreboard(scoreboard):
    categories = list(strategies.keys())

    for category in categories:
        if category in scoreboard:
            print(category, scoreboard[category])
        else:
            print(category, 0)

def get_score_for_category(category, roll, scoreboard):
    return strategies[category]["f"](user_roll, scoreboard["bonus_yahtzees"])

user_roll = []
keep_numbers = []
available_categories = list(strategies.keys())
scoreboard = {"bonus_yahtzees": 0}


while len(available_categories) > 0:
    for i in range(3):
        user_roll = roll(user_roll, keep_numbers)
        print(" ".join([str(r) for r in user_roll]))
        keep_numbers = get_keep_numbers(user_roll)
        if (len(keep_numbers) == 5):
            break
    print("final roll:", " ".join([str(r) for r in user_roll]))
    for category in available_categories:
        (score, is_yahtzee) = get_score_for_category(category, user_roll, scoreboard)
        if is_yahtzee:
            print(category, score, "YAHTZEE!")
        else:
            print(category, score)
    chosen_category = input("what category do you want to use?\n")
    while chosen_category not in available_categories:
        print("invalid category")
        chosen_category = input("what category do you want to use?\n")
        continue
    (score, is_yahtzee) = get_score_for_category(chosen_category, user_roll, scoreboard)
    scoreboard[chosen_category] = score
    if is_yahtzee:
        scoreboard["bonus_yahtzees"] += 1
    # remove the category from the list of available categories
    available_categories.remove(chosen_category)
    user_roll = []
    keep_numbers = []
    # clear screen
    print("\033c")
    print("current scoreboard: ")
    show_scoreboard(scoreboard)
    input("press any key to continue")
    print("\033c")

print("THE GAME IS OVER!")
show_scoreboard(scoreboard)
print("final score:", final_score(scoreboard))