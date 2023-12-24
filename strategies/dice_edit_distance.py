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

def test_pair(d1, d2):
    print(d1, d2, dice_edit_distance(d1, d2))

test_pair("11111", "11111")
test_pair("11111", "11112")
test_pair("11111", "11113")
test_pair("11111", "11114")
test_pair("11111", "11115")
test_pair("11111", "11116")
test_pair("11111", "11122")
test_pair("11111", "11123")
test_pair("11111", "11124")
test_pair("11111", "11125")
test_pair("11111", "22222")
test_pair("12345", "23456")
test_pair("12345", "23456")
test_pair("11111", "12223")
