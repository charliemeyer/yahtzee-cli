import random
from strategies.scores import strategies, get_score_for_category

def get_keep_numbers(roll, _a, _b):
    freqs = {}
    for d in roll:
        if d in freqs:
            freqs[d] += 1
        else:
            freqs[d] = 1
    best_freq = 0
    choice = 0
    for d in freqs:
        if freqs[d] > best_freq:
            best_freq = freqs[d]
            choice = d
    return [choice for _ in range(best_freq)]


def get_category_choice(available_categories, roll, scoreboard):
    fracs_and_scores = []
    for category in available_categories:
        (score, _)  = get_score_for_category(category, roll, scoreboard)
        max = strategies[category]["max"]
        fracs_and_scores.append((score/max, score, category))
    fracs_and_scores.sort(reverse=True)
    return fracs_and_scores[0][2]