import random
from yahtzee.scores import categories, get_final_score, get_score_for_category
import curses

def get_roll(keep_numbers):
    new_roll = []
    for i in range(5):
        if i < len(keep_numbers):
            new_roll.append(keep_numbers[i])
        else:
            new_roll.append(random.randint(1,6))
    return sorted(new_roll)

def cat_name_to_display_name(cat_name):
    return cat_name.replace("_", " ").title()

class Yahtzee():
    def __init__(self, strategy, interactive, stdscr):
        self.scoreboard = {"num_yahtzees": 0}
        self.available_categories = list(categories.keys())
        self.strategy = strategy
        self.interactive = interactive
        self.stdscr = stdscr

    def log(self, *messages):
        self.stdscr.addstr(" ".join([str(m) for m in messages]) + "\n")

    def show_scoreboard(self):
        cats = list(categories.keys())
        total_score = 0
        self.log("Scoreboard:")
        self.log("-----------")
        for idx, cat in enumerate(cats):
            if idx == 6:
                self.log("-----------")
            display_name = cat_name_to_display_name(cat)
            if cat in self.scoreboard:
                score = self.scoreboard[cat]
                if score == 0:
                    self.log(display_name, "X")
                else:
                    self.log(display_name, score)
                total_score += score
            else:
                self.log(display_name, 0)
        self.log("Total yahtzees:", self.scoreboard["num_yahtzees"])
        self.log("")
        self.log("Press enter to continue")

    def run(self):
        roll = []
        keep_numbers = []
        while len(self.available_categories) > 0:
            roll = get_roll(keep_numbers)
            for i in range(2):
                if self.interactive:
                    keep_number_choices = self.strategy.get_ranked_keep_numbers(roll, self.available_categories, i)
                    keep_numbers = self.get_user_keep_numbers(roll, keep_number_choices)
                else:
                    keep_numbers = self.strategy.get_keep_number_choice(roll, self.available_categories, i)
                if (len(keep_numbers) == 5):
                    break
                roll = get_roll(keep_numbers)
            chosen_category = ""
            if self.interactive:
                self.log("Final roll:", " ".join([str(r) for r in roll]))
                category_choices = self.strategy.get_ranked_category_choices(self.available_categories, roll, self.scoreboard)
                options_to_show = []
                for category in category_choices:
                    (score, _) = get_score_for_category(category, roll, self.scoreboard)
                    options_to_show.append((category, score))
                chosen_category = self.get_user_category_choice(roll, options_to_show)
            else:
                chosen_category = self.strategy.get_category_choice(self.available_categories, roll, self.scoreboard)
            (score, is_yahtzee) = get_score_for_category(chosen_category, roll, self.scoreboard)
            self.scoreboard[chosen_category] = score
            if is_yahtzee:
                self.scoreboard["num_yahtzees"] += 1
            self.available_categories.remove(chosen_category)
            roll = []
            keep_numbers = []
            if self.interactive:
                self.show_scoreboard()
                self.stdscr.getch()

        final_score = get_final_score(self.scoreboard)
        if self.interactive:
            self.stdscr.clear()
            self.log("Final score:", final_score)
            self.stdscr.getch()

        return final_score

    def get_user_keep_numbers(self, roll, keep_number_choices):
        current_row = 0
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "Roll: " + " ".join([str(r) for r in roll]))
            self.stdscr.addstr(1, 0, "----------")

            for idx, item in enumerate(keep_number_choices):
                to_show = f"{' '.join([str(d) for d in item[0]])} ({str(item[1])})"
                if idx == current_row:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(idx + 2, 0, to_show)
                    self.stdscr.attroff(curses.color_pair(1))
                else:
                    self.stdscr.attron(curses.color_pair(2))
                    self.stdscr.addstr(idx + 2, 0, to_show)
                    self.stdscr.attroff(curses.color_pair(2))

            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(keep_number_choices) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                break

            self.stdscr.refresh()
        self.stdscr.clear()
        return keep_number_choices[current_row][0]

    def get_user_category_choice(self, roll, available_categories):
        current_row = 0
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "Final roll: " + " ".join([str(r) for r in roll]))
            self.stdscr.addstr(1, 0, "----------")

            for idx, item in enumerate(available_categories):
                to_show = display_name = cat_name_to_display_name(item[0]) + " " + str(item[1])
                if idx == current_row:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(idx + 2, 0, to_show)
                    self.stdscr.attroff(curses.color_pair(1))
                else:
                    self.stdscr.attron(curses.color_pair(2))
                    self.stdscr.addstr(idx + 2, 0, to_show)
                    self.stdscr.attroff(curses.color_pair(2))

            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(available_categories) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                break

            self.stdscr.refresh()
        self.stdscr.clear()
        return available_categories[current_row][0]