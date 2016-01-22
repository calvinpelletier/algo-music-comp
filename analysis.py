# analysis.py
# Calvin Pelletier
# 1/21/16

import math

def analyze_characteristics(melodies):
    energies = []
    progression_dissonances = []
    key_dissonances = []
    rhythmics = []
    for m in melodies:
        energies.append(m.energy)
        progression_dissonances.append(m.progression_dissonance)
        key_dissonances.append(m.key_dissonance)
        rhythmics.append(m.rhythmic)
    print("\nenergy avg: %f\nenergy std_dev: %f\n\n\
progression_dissonance avg: %f\nprogression_dissonance std_dev: %f\n\n\
key_dissonance avg: %f\nkey_dissonance std_dev: %f\n\n\
rhythmic avg: %f\nrhythmic std_dev: %f\n" % \
        (average(energies), std_dev(energies),\
        average(progression_dissonances), std_dev(progression_dissonances),\
        average(key_dissonances), std_dev(key_dissonances),\
        average(rhythmics), std_dev(rhythmics)))

def average(data):
    total = 0.0
    for d in data:
        total += d
    return total / float(len(data))

def std_dev(data):
    avg = average(data)
    total = 0.0
    for d in data:
        total += abs(d - avg)**2
    return math.sqrt(total / float(len(data)))
