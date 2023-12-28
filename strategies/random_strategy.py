import random
from strategies.Strategy import Strategy

class CompletelyRandom(Strategy):
    def get_ranked_keep_numbers(self, roll, _a, _b):
        return roll
    
    def get_keep_number_choice(self, roll, _available_categories, _roll_number):
        return roll

    def get_ranked_category_choices(self, available_categories, _roll, _scoreboard):
        return random.choice(available_categories)
    
    def get_category_choice(self, available_categories, roll, scoreboard):
        ranked_choices = self.get_ranked_category_choices(available_categories, roll, scoreboard)
        return random.choice(ranked_choices)
