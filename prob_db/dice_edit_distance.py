import math

def get_freqs(roll):
    freqs = {}
    for d in roll:
        if d in freqs:
            freqs[d] += 1
        else:
            freqs[d] = 1
    return freqs

def dice_edit_distance(keep, roll2):
    freqs2 = get_freqs(roll2)
    keep_freqs = get_freqs(keep)
    changes = []
    for d in freqs2:
        old_freq = keep_freqs[d] if d in keep_freqs else 0
        if freqs2[d] > old_freq:
            changes.append(freqs2[d] - old_freq)
    
    if len(changes) == 0:
        return 1
    
    permutation_count = math.factorial(sum(changes)) / math.prod([math.factorial(c) for c in changes])
    return permutation_count * ((1 / 6) ** sum(changes))
