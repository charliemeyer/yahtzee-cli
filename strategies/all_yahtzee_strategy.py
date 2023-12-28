from yahtzee.scores import categories, get_score_for_category
from strategies.Strategy import Strategy

class AllYahtzee(Strategy):
    def get_ranked_keep_numbers(self, roll, _a, _b):
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
        return [[choice for _ in range(best_freq)]]

    def get_keep_number_choice(self, roll, available_categories, roll_number):
        return self.get_ranked_keep_numbers(roll, available_categories, roll_number)[0]

    def get_ranked_category_choices(self, available_categories, roll, scoreboard):
        fracs_and_scores = []
        for category in available_categories:
            (score, _)  = get_score_for_category(category, roll, scoreboard)
            max = categories[category]["max"]
            fracs_and_scores.append((score/max, score, category))
        fracs_and_scores.sort(reverse=True)
        return [fracs_and_scores[0][2]]
    
    def get_category_choice(self, available_categories, roll, scoreboard):
        return self.get_ranked_category_choices(available_categories, roll, scoreboard)[0]