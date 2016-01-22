# chord.py
# Calvin Pelletier
# 1/20/16

import note
import music21

class Chord:
    def __init__(self, numeral):
        self.numeral = numeral
    def dissonance_of_note(self, n):
        DISSONANCE = {}
        DISSONANCE['I']   = [0.0, 1.0, 0.1, 1.0, 0.0, 1.0, 0.6]
        DISSONANCE['ii']  = [0.6, 0.0, 1.0, 0.1, 1.0, 0.0, 1.0]
        DISSONANCE['iii'] = [1.0, 1.0, 0.0, 1.0, 0.1, 1.0, 0.0]
        DISSONANCE['III'] = [1.0, 1.0, 0.0, 1.0, 9.9, 1.0, 0.0]
        DISSONANCE['IV']  = [0.0, 1.0, 0.6, 0.0, 1.0, 0.1, 1.0]
        DISSONANCE['V']   = [1.0, 0.0, 1.0, 0.4, 0.0, 1.0, 0.1]
        DISSONANCE['vi']  = [0.1, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0]
        return DISSONANCE[self.numeral][n.degree - 1]
    def get_music21(self):
        k = music21.key.Key('C')
        return music21.roman.RomanNumeral(self.numeral, k)
