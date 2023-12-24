import math

def get_freqs(roll):
    freqs = {}
    for d in roll:
        if d in freqs:
            freqs[d] += 1
        else:
            freqs[d] = 1
    return freqs

def dice_edit_distance(roll1, roll2):
    freqs1 = get_freqs(roll1)
    freqs2 = get_freqs(roll2)
    changes = []
    for d in freqs2:
        old_freq = freqs1[d] if d in freqs1 else 0
        if freqs2[d] > old_freq:
            changes.append(freqs2[d] - old_freq)
    prob = 1
    for change in changes:
        prob *= (1/6) ** change
    prob *= math.factorial(len(changes))
    return prob
