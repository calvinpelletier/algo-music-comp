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
        ret = music21.roman.RomanNumeral(self.numeral, k)
        if self.numeral == 'I':
            ret.transpose(-7, inPlace=True)
        elif self.numeral == 'ii':
            ret.transpose(-19, inPlace=True)
        elif self.numeral == 'iii':
            ret.transpose(-19, inPlace=True)
        elif self.numeral == 'III':
            ret.transpose(-19, inPlace=True)
        elif self.numeral == 'IV':
            ret.transpose(-19, inPlace=True)
            ret.inversion(2)
        elif self.numeral == 'V':
            ret.transpose(-19, inPlace=True)
            ret.inversion(1)
        elif self.numeral == 'vi':
            ret.transpose(-19, inPlace=True)
            ret.inversion(1)
        return ret
