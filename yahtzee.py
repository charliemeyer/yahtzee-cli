import random
from strategies.scores import strategies, final_score, get_score_for_category
import sys

import strategies.human_strategy as human_strategy
import strategies.random_ai as random_strategy
import strategies.all_yahtzee as all_yahtzee_strategy
import strategies.random_greedy_ai as random_greedy_strategy
import strategies.greedy_level_1_prob_strategy as greedy_level_1_prob_strategy
import strategies.greedy_level_2_prob_strategy as greedy_level_2_prob_strategy
import strategies.level1_plus_chance_heuristic as level_1_plus_chance_heuristic_strategy
import strategies.level1_with_difficulty as level_1_with_difficulty_strategy

import matplotlib.pyplot as plt
import numpy as np

quiet_mode = False

def log(*messages):
    if quiet_mode:
        return
    print(*messages)

def roll(keep_numbers):
    new_roll = []
    for i in range(5):
        if i < len(keep_numbers):
            new_roll.append(keep_numbers[i])
        else:
            new_roll.append(random.randint(1,6))
    return sorted(new_roll)

def show_scoreboard(scoreboard):
    categories = list(strategies.keys())

    for category in categories:
        if category in scoreboard:
            log(category, scoreboard[category])
        else:
            log(category, 0)
    log("num yahtzees", scoreboard["num_yahtzees"])

def run_game(scoreboard, available_categories, strategy):
    user_roll = []
    keep_numbers = []
    while len(available_categories) > 0:
        user_roll = roll(keep_numbers)
        for i in range(2):
            log(" ".join([str(r) for r in user_roll]))
            keep_numbers = strategy.get_keep_numbers(user_roll, available_categories, i)
            if (len(keep_numbers) == 5):
                break
            user_roll = roll(keep_numbers)
        log("final roll:", " ".join([str(r) for r in user_roll]))
        for category in available_categories:
            (score, is_yahtzee) = get_score_for_category(category, user_roll, scoreboard)
            if is_yahtzee:
                log(category, score, "YAHTZEE!")
            else:
                log(category, score)
        chosen_category = strategy.get_category_choice(available_categories, user_roll, scoreboard)
        (score, is_yahtzee) = get_score_for_category(chosen_category, user_roll, scoreboard)
        scoreboard[chosen_category] = score
        if is_yahtzee:
            scoreboard["num_yahtzees"] += 1
        # remove the category from the list of available categories
        available_categories.remove(chosen_category)
        user_roll = []
        keep_numbers = []
        # clear screen
        # log("\033c")
        log("current scoreboard: ")
        show_scoreboard(scoreboard)
        # log("\033c")
    return final_score(scoreboard)

def main():
    global quiet_mode

    strategy = None
    strategy_choice = sys.argv[1]
    if strategy_choice == "human":
        strategy = human_strategy
    if strategy_choice == "random":
        strategy = random_strategy
    if strategy_choice == "all_yahtzee":
        strategy = all_yahtzee_strategy
    if strategy_choice == "random_greedy":
        strategy = random_greedy_strategy
    if strategy_choice == "greedy_prob2":
        strategy = greedy_level_2_prob_strategy
    if strategy_choice == "greedy_prob1":
        strategy = greedy_level_1_prob_strategy
    if strategy_choice == "level1_plus_chance":
        strategy = level_1_plus_chance_heuristic_strategy
    if strategy_choice == "level1_with_difficulty":
        strategy = level_1_with_difficulty_strategy
    
    num_runs = int(sys.argv[2])
    if num_runs > 1:
        quiet_mode = True

    sum_scores = 0
    scores = []
    for i in range(num_runs):
        available_categories = list(strategies.keys())
        scoreboard = {"num_yahtzees": 0}
        score = run_game(scoreboard, available_categories, strategy)
        sum_scores += score
        scores.append(score)
        log("score", score)
        if not quiet_mode:
            input("press any key to continue")
        log("THE GAME IS OVER!")
        show_scoreboard(scoreboard)
        log("final score:", score)
    # Calculate the median
    median_score = np.median(scores)

    # Create the histogram
    plt.hist(scores, bins=100, edgecolor='black', alpha=0.7)

    # Add a red vertical line at the median
    plt.axvline(median_score, color='red', linestyle='dashed', linewidth=2)

    # Annotate the median value
    plt.text(median_score, plt.ylim()[1]*0.9, f'Median: {median_score}', color = 'red')

    # Adding titles and labels
    plt.title('Histogram of Scores with Median')
    plt.xlabel('Scores')
    plt.ylabel('Frequency')

    # Display the plot
    plt.show()
    print("average score", sum_scores / num_runs)

main()