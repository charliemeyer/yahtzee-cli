import random
from scores import strategies, final_score
import sys

import human_strategy


def roll(old_roll, keep_numbers):
    new_roll = []
    for i in range(5):
        if i < len(keep_numbers):
            # TODO: check if the keep number is actually legit
            new_roll.append(keep_numbers[i])
        else:
            new_roll.append(random.randint(1,6))
    return sorted(new_roll)



def show_scoreboard(scoreboard):
    categories = list(strategies.keys())

    for category in categories:
        if category in scoreboard:
            print(category, scoreboard[category])
        else:
            print(category, 0)

def get_score_for_category(category, roll, scoreboard):
    return strategies[category]["f"](roll, scoreboard["bonus_yahtzees"])

def interactive_mode(scoreboard, available_categories, strategy):
    user_roll = []
    keep_numbers = []
    while len(available_categories) > 0:
        for _ in range(3):
            user_roll = roll(user_roll, keep_numbers)
            print(" ".join([str(r) for r in user_roll]))
            keep_numbers = strategy.get_keep_numbers(user_roll)
            if (len(keep_numbers) == 5):
                break
        print("final roll:", " ".join([str(r) for r in user_roll]))
        for category in available_categories:
            (score, is_yahtzee) = get_score_for_category(category, user_roll, scoreboard)
            if is_yahtzee:
                print(category, score, "YAHTZEE!")
            else:
                print(category, score)
        chosen_category = strategy.get_category_choice(available_categories, scoreboard)
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

def main():
    available_categories = list(strategies.keys())
    scoreboard = {"bonus_yahtzees": 0}
    interactive_mode(scoreboard, available_categories, human_strategy)

    print("THE GAME IS OVER!")
    show_scoreboard(scoreboard)
    print("final score:", final_score(scoreboard))

main()