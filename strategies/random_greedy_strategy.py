from yahtzee.scores import get_score_for_category
from strategies.Strategy import Strategy

class RandomGreedy(Strategy):
    def get_ranked_keep_numbers(self, _roll, _a, _b):
        return []
    
    def get_keep_number_choice(self, roll, available_categories, roll_number):
        return roll

    def get_ranked_category_choices(self, available_categories, roll, scoreboard):
        best_category = available_categories[0]
        best_score = get_score_for_category(available_categories[0], roll, scoreboard)
        for category in available_categories:
            score = get_score_for_category(category, roll, scoreboard)
            if score > best_score:
                best_score = score
                best_category = category
        return best_category
    
    def get_category_choice(self, available_categories, roll, scoreboard):
        return RandomGreedy.get_ranked_category_choices(available_categories, roll, scoreboard)[0]