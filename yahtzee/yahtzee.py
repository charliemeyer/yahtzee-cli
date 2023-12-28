import random
from yahtzee.scores import categories, get_final_score, get_score_for_category

def get_roll(keep_numbers):
    new_roll = []
    for i in range(5):
        if i < len(keep_numbers):
            new_roll.append(keep_numbers[i])
        else:
            new_roll.append(random.randint(1,6))
    return sorted(new_roll)

def get_user_keep_numbers(roll):
    good_keep_numbers = False
    keep_numbers = []

    while not good_keep_numbers:
        keep_choice = input("What dice do you want to keep? (\"all\" to keep all, \"none\" to keep none)\n")
        if keep_choice == "all":
            return roll
        try:
            keep_numbers = [] if keep_choice == "none" else [int(n) for n in keep_choice]
            good_keep_numbers = True
        except:
            print("Invalid choice")
            continue
        if keep_choice == "all":
            break
        for n in keep_numbers:
            if n not in roll:
                print("Invalid keep number")
                good_keep_numbers = False
                break
    return keep_numbers


def get_user_category_choice(available_categories):
    chosen_category = input("What category do you want to use?\n")
    while chosen_category not in available_categories:
        print(chosen_category, " is an invalid category")
        chosen_category = input("What category do you want to use?\n")
        continue
    return chosen_category

class Yahtzee():
    quiet_mode = False

    def __init__(self, strategy, interactive):
        self.scoreboard = {"num_yahtzees": 0}
        self.available_categories = list(categories.keys())
        self.strategy = strategy
        self.quiet = not interactive
        self.interactive = interactive

    def log(self, *messages):
        if self.quiet:
            return
        print(*messages)

    def show_scoreboard(self):
        cats = list(categories.keys())

        for cat in cats:
            if cat in self.scoreboard:
                self.log(cat, self.scoreboard[cat])
            else:
                self.log(cat, 0)
        self.log("num yahtzees", self.scoreboard["num_yahtzees"])

    def run(self):
        roll = []
        keep_numbers = []
        while len(self.available_categories) > 0:
            roll = get_roll(keep_numbers)
            for i in range(2):
                self.log(" ".join([str(r) for r in roll]))
                if self.interactive:
                    keep_numbers = get_user_keep_numbers(roll)
                else:
                    keep_numbers = self.strategy.get_keep_number_choice(roll, self.available_categories, i)
                if (len(keep_numbers) == 5):
                    break
                roll = get_roll(keep_numbers)
            self.log("Final roll:", " ".join([str(r) for r in roll]))
            for category in self.available_categories:
                (score, is_yahtzee) = get_score_for_category(category, roll, self.scoreboard)
                if is_yahtzee:
                    self.log(category, score, "YAHTZEE!")
                else:
                    self.log(category, score)
            chosen_category = ""
            if self.interactive:
                chosen_category = get_user_category_choice(self.available_categories)
            else:
                chosen_category = self.strategy.get_category_choice(self.available_categories, roll, self.scoreboard)
            (score, is_yahtzee) = get_score_for_category(chosen_category, roll, self.scoreboard)
            self.scoreboard[chosen_category] = score
            if is_yahtzee:
                self.scoreboard["num_yahtzees"] += 1
            self.available_categories.remove(chosen_category)
            roll = []
            keep_numbers = []
            # clear screen
            self.log("\033c")
            self.show_scoreboard()
            self.log("\033c")

        return get_final_score(self.scoreboard)