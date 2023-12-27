from strategies.scores import strategies, get_score_for_category

def get_keep_numbers(roll, _a, _b):
    return roll

def get_category_choice(available_categories, roll, scoreboard):
    best_category = available_categories[0]
    best_score = get_score_for_category(available_categories[0], roll, scoreboard)
    for category in available_categories:
        score = get_score_for_category(category, roll, scoreboard)
        if score > best_score:
            best_score = score
            best_category = category
    return best_category