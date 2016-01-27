# analysis.py
# Calvin Pelletier
# 1/21/16

import math

def analyze_characteristics(melodies):
    characteristics = {}
    for m in melodies:
        for key, value in m.characteristics.iteritems():
            if characteristics.has_key(key):
                characteristics[key].append(value)
            else:
                characteristics[key] = [value]
    for key, value in characteristics.iteritems():
        print("%s avg: %f\n%s std_dev: %f\n" % (key, average(value), key, std_dev(value)))

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
