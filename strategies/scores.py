def num(roll, target):
    score = 0
    for d in roll:
        if d == target:
            score += d
    return score

def ones(roll):
    return num(roll, 1)

def twos(roll):
    return num(roll, 2)

def threes(roll):
    return num(roll, 3)

def fours(roll):
    return num(roll, 4)

def fives(roll):
    return num(roll, 5)

def sixes(roll):
    return num(roll, 6)

def three_of_kind(roll):
    freqs = {}
    for d in roll:
        if d in freqs:
            freqs[d] += 1
        else:
            freqs[d] = 1
    for d in freqs:
        if freqs[d] >= 3:
            return sum(roll)
    return 0

def four_of_kind(roll):
    freqs = {}
    for d in roll:
        if d in freqs:
            freqs[d] += 1
        else:
            freqs[d] = 1
    for d in freqs:
        if freqs[d] >= 4:
            return sum(roll)
    return 0
    
def full_house(roll):
    freqs = {}
    for d in roll:
        if d in freqs:
            freqs[d] += 1
        else:
            freqs[d] = 1
    for d in freqs:
        if freqs[d] == 3:
            for d in freqs:
                if freqs[d] == 2:
                    return 25
    return 0

def large_straight(roll):
    sorted_roll = "".join([str(s) for s in sorted(roll)])
    return 40 if sorted_roll == "12345" else 0

def small_straight(roll):
    distinct = "".join([str(s) for s in sorted(list(set(roll)))])
    if "1234" in distinct or "2345" in distinct or "3456" in distinct:
        return 30
    return 0

def yahtzee(roll):
    for d in roll:
        if d != roll[0]:
            return 0
    return 50

def chance(roll):
    return sum(roll)

def wrapped_strat(strat):
    def wrapped(roll, num_yahtzees):
        strat_f = strategies[strat]["original_f"]
        original_score = strat_f(roll)
        is_yahtzee = yahtzee(roll) == 50
        if is_yahtzee and num_yahtzees > 0:
            return (strategies[strat]["max"], is_yahtzee)
        return (original_score, is_yahtzee)
    return wrapped


strategies = {
    "ones": {
        "f": wrapped_strat("ones"),
        "original_f": ones,
        "max": 5
    },
    "twos": {
        "f": wrapped_strat("twos"),
        "original_f": twos,
        "max": 10
    },
    "threes": {
        "f": wrapped_strat("threes"),
        "original_f": threes,
        "max": 15
    },
    "fours": {
        "f": wrapped_strat("fours"),
        "original_f": fours,
        "max": 20,
    },
    "fives": {
        "f": wrapped_strat("fives"),
        "original_f": fives,
        "max": 25,
    },
    "sixes": {
        "f": wrapped_strat("sixes"),
        "original_f": sixes,
        "max": 30,
    },
    "three_of_kind": {
        "f": wrapped_strat("three_of_kind"),
        "original_f": three_of_kind,
        "max": 30,
    },
    "four_of_kind": {
        "f": wrapped_strat("four_of_kind"),
        "original_f": four_of_kind,
        "max": 30
    },
    "full_house": {
        "f": wrapped_strat("full_house"),
        "original_f": full_house,
        "max": 25
    },
    "small_straight": {
        "f": wrapped_strat("small_straight"),
        "original_f": small_straight,
        "max": 30
    },
    "large_straight": {
        "f": wrapped_strat("large_straight"),
        "original_f": large_straight,
        "max": 40,
    },
    "yahtzee": {
        "f": wrapped_strat("yahtzee"),
        "original_f": yahtzee,
        "max": 50
    },
    "chance": {
        "f": wrapped_strat("chance"), 
        "original_f": chance,
        "max": 30
    }
}




def score_options(roll, available_categories):
    category_scores = {}
    for c in available_categories:
        category_scores[c] = strategies[c](roll)
    return category_scores

def final_score(scoreboard):
    score = 0
    upper_score = scoreboard["ones"] + scoreboard["twos"] + scoreboard["threes"] + scoreboard["fours"] + scoreboard["fives"] + scoreboard["sixes"]
    if upper_score >= 63:
        score += 35
    score += upper_score
    score += scoreboard["three_of_kind"]
    score += scoreboard["four_of_kind"]
    score += scoreboard["full_house"]
    score += scoreboard["small_straight"]
    score += scoreboard["large_straight"]
    score += scoreboard["yahtzee"]
    score += scoreboard["chance"]
    if scoreboard["num_yahtzees"] > 1:
        score += 100 * (scoreboard["num_yahtzees"] - 1)
    return score

def get_score_for_category(category, roll, scoreboard):
    return strategies[category]["f"](roll, scoreboard["num_yahtzees"])