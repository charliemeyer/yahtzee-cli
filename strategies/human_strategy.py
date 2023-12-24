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
            if n not in roll:
                print("invalid keep number")
                good_keep_numbers = False
                break
    return keep_numbers


def get_category_choice(available_categories, _roll, _scoreboard):
    chosen_category = input("what category do you want to use?\n")
    while chosen_category not in available_categories:
        print("invalid category")
        chosen_category = input("what category do you want to use?\n")
        continue
    return chosen_category