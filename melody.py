# melody.py
# Calvin Pelletier
# 1/1/16

from music21 import *
from random import randint, random
import progression

# melody in string format: x 1,1 - 1,2 - - x x | 3,1
# | is a measure divider, x is a rest, - is a continuation of the previous note, 1,2 is the 1 note (relative to key) in the 2nd octave

# NOTE: EVERYTHING IS HANDLED AS IF IT'S IN THE KEY OF C MAJOR/A MINOR
# IF IT'S IN A MINOR, 1 STILL REPRESENTS C, BUT ITS CHARACTERISTICS ACCOUNT FOR THE DIFFERENCES BETWEEN C MAJOR AND A MINOR

class Melody:
    # MELODY
    m = stream.Part()

    # HELPER INFORMATION
    progression = []
    minor = False
    rhythmic_style = 0 # see rhythmic()

    # CHARACTERISTICS
    energy = 0.0 # average of intervals divided by durations
    rhythmic = 0.0
    progression_dissonance = 0.0
    key_dissonance = 0.0
    thematic = 0.0 # amount of repetition

    # INITIALIZATION FUNCTIONS
    def __init__(self, m):
        if isinstance(m, stream.Part):
            self.m = m
        elif isinstance(m, basestring):
            self.m = melody_from_string(m)
        else:
            raise NameError("Undefined melody format.")

    # CHARACTERISTIC FUNCTIONS
    def calculate_all_characteristics(self):
        self.energy()
        self.progression_dissonance()
        self.key_dissonance()
        self.rhythmic()

    def energy(self):
        total = 0.0
        notes = self.m.flat.getElementsByClass(note.Note)
        for i in range(len(notes) - 1):
            total += abs(interval.notesToChromatic(notes[i], notes[i + 1]).semitones) / float(notes[i].quarterLength)
        self.energy = total / float(len(notes))

    def progression_dissonance(self):
        if len(self.progression) == 0:
            raise NameError("Tried to calculate progression dissonance without first specifying a progression.")

        CHORD_DURATION_DOUBLED = 8
        progression_duration_doubled = CHORD_DURATION_DOUBLED * len(self.progression)

        total = 0.0
        for n in self.m.flat.getElementsByClass(note.Note):
            for i in range(int(n.offset * 2), int((n.offset + n.quarterLength) * 2)):
                chord = self.progression[(i % progression_duration_doubled) / CHORD_DURATION_DOUBLED]
                total += progression.dissonance(chord.romanNumeral, n.name)
        self.progression_dissonance = total / float(len(self.m.flat.getElementsByClass(note.Note)))

    def key_dissonance(self):
        # favors 1 and 5 primarily, then the pentatonic scale
        #                    1    2    3    4    5    6    7
        DISSONANCE_MAJOR = {'C':0.0, 'D':0.4, 'E':0.4, 'F':0.7, 'G':0.2, 'A':0.4, 'B':1.0}
        DISSONANCE_MINOR = {'C':0.4, 'D':0.4, 'E':0.2, 'F':0.7, 'G':0.4, 'A':0.0, 'B':1.0}

        total = 0.0
        i = 0
        for n in self.m.flat.getElementsByClass(note.Note):
            if self.minor:
                total += DISSONANCE_MINOR[n.name] * n.quarterLength
            else:
                total += DISSONANCE_MAJOR[n.name] * n.quarterLength
        self.key_dissonance = total / float(len(self.m.flat.getElementsByClass(note.Note)))

    #def thematic(arr_melody):

    def rhythmic(self):
        #                       1   and   2   and   3   and   4   and
        RHYTHMIC_STYLE = []
        RHYTHMIC_STYLE.append([1.0, 0.0, 0.5, 0.0, 0.7, 0.0, 0.5, 0.0]) # style 0
        RHYTHMIC_STYLE.append([0.0, 1.0, 0.0, 0.5, 0.0, 0.7, 0.0, 0.5]) # style 1
        RHYTHMIC_STYLE.append([0.5, 0.0, 1.0, 0.0, 0.5, 0.0, 0.7, 0.0]) # style 2
        RHYTHMIC_STYLE.append([0.0, 0.5, 0.0, 1.0, 0.0, 5.0, 0.0, 0.7]) # style 3

        total = 0.0
        for n in self.m.flat.getElementsByClass(note.Note):
            total += RHYTHMIC_STYLE[self.rhythmic_style][int(n.offset * 2) % 8] * n.quarterLength
        self.rhythmic = total / float(len(self.m.flat.getElementsByClass(note.Note)))

    #def rhythmic_variation(melody):

    #def tonal_variation(melody):

    #HELPER FUNCTIONS
    def printable_progression(self):
        ret = []
        for chord in self.progression:
            ret.append(chord.romanNumeral)
        return '-'.join(ret)

    def show(self, param='default'):
        if param == 'default':
            self.m.show()
        else:
            self.m.show(param)

def melody_from_string(string):
    ret = stream.Part()
    src = string.split(' ')
    i = 0
    while i < len(src):
        if src[i] == 'x':
            cur = note.Rest()
        elif src[i] == '-':
            i += 1
            continue
        elif src[i] == '|':
            i += 1
            continue
        elif len(src[i]) == 3:
            cur = note.Note(note_from_string(src[i]))
        else:
            raise NameError("error parsing melody from string")
        cur.quarterLength = 0.5
        i += 1
        while i < len(src):
            if src[i] == '|':
                if isinstance(cur, note.Rest):
                    break
            elif src[i] == '-':
                cur.quarterLength += 0.5
            elif src[i] == 'x' and isinstance(cur, note.Rest):
                cur.quarterLength += 0.5
            else:
                break
            i += 1
        ret.append(cur)
    return ret

def note_from_string(string):
    if string[0] == '1':
        ret = 'C'
    elif string[0] == '2':
        ret = 'D'
    elif string[0] == '3':
        ret = 'E'
    elif string[0] == '4':
        ret = 'F'
    elif string[0] == '5':
        ret = 'G'
    elif string[0] == '6':
        ret = 'A'
    elif string[0] == '7':
        ret = 'B'
    else:
        raise NameError("error parsing note from string")
    return ret + string[2]

#def music21_from_exact_note(note):
#    note_dict = {1:'C', 2:'D', 3:'E', 4:'F', 5:'G', 6:'A', 7:'B'}
#    return note.Note(note_dict[(note - 1) % 7 + 1] + str((note - 1) / 7 + 1))

#def note_octave_to_exact_note(note, octave):
#    return note + 7 * (octave - 1)

# returns in str format: 1,4
#def exact_note_to_note_octave(note):
#    octave = (note - 1) / 7 + 1
#    note_in_octave = (note - 1) % 7 + 1
#    return str(note_in_octave) + ',' + str(octave)

def create_random_melody():
    MAX_RANGE = 20 # in semitones
    UPPER_NOTE_BOUND = note.Note('G5')
    LOWER_NOTE_BOUND = note.Note('G3')
    UPPER_LEN_BOUND = 16 # in measures
    LOWER_LEN_BOUND = 4
    POSSIBLE_START_NOTES = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
    CHANCE_OF_REST = 0.1
    CHANCE_OF_EXTENSION = 0.4
    MINOR_CHANCE = 0.5

    m = stream.Part()
    m.insert(instrument.Flute())
    length = 4.0 * randint(LOWER_LEN_BOUND, UPPER_LEN_BOUND)
    s = scale.MajorScale('C')
    start_note = note.Note(POSSIBLE_START_NOTES[randint(0, len(POSSIBLE_START_NOTES) - 1)])
    m.append(start_note)
    lowest_note = start_note
    highest_note = start_note
    while(m.quarterLength < length):
        rand = random()
        if rand < CHANCE_OF_REST:
            if isinstance(m[-1], note.Rest):
                m[-1].quarterLength += 0.5
            else:
                temp = note.Rest()
                temp.quarterLength = 0.5
                m.append(temp)
        elif rand < CHANCE_OF_REST + CHANCE_OF_EXTENSION:
            m[-1].quarterLength += 0.5
        else:
            notes = m.getElementsByClass(note.Note)
            rand = random()
            if rand < 0.5:
                direction = 'ascending'
            else:
                direction = 'descending'
            temp = s.next(notes[-1], direction, randint(1,7))
            while   temp < LOWER_NOTE_BOUND.pitch or\
                    temp > UPPER_NOTE_BOUND.pitch or\
                    temp < highest_note.transpose(MAX_RANGE * -1) or\
                    temp > lowest_note.transpose(MAX_RANGE):
                rand = random()
                if rand < 0.5:
                    direction = 'ascending'
                else:
                    direction = 'descending'
                temp = s.next(notes[-1], direction, randint(1,7))
            temp = note.Note(temp)
            if temp.pitch < lowest_note.pitch:
                lowest_note = temp
            if temp.pitch > highest_note.pitch:
                highest_note = temp
            temp.quarterLength = 0.5
            m.append(temp)

    ret = Melody(m)
    ret.minor = randint(0, 100) / 100.0 < MINOR_CHANCE
    return ret

def print_melody(melody):
    print("~~~%s (%s)~~~:\n %s\nenergy: %f\nprogression_dissonance: %f\nkey_dissonance: %f\nrhythmic: %f\n" \
       % (melody.m.id, melody.printable_progression(), "TODO", melody.energy, melody.progression_dissonance, melody.key_dissonance, melody.rhythmic))

def run_test_data():
    melody_data = open('melody_data.txt', 'r')
    melodies = []
    while 1:
        title = melody_data.readline().rstrip('\n')
        majorminor = melody_data.readline().rstrip('\n')
        rhythmic_style = melody_data.readline().rstrip('\n')
        melody = melody_data.readline().rstrip('\n')
        pre_progression = melody_data.readline().rstrip('\n')
        if title == '' or majorminor == '' or melody == '' or progression == '':
            break
        temp = Melody(melody)
        temp.m.id = title
        if majorminor == 'major' or majorminor == 'Major':
            temp.minor = False
        elif majorminor == 'minor' or majorminor == 'Minor':
            temp.minor = True
        else:
            raise NameError("Expected result for Major/Minor when parsing melody test data")
        temp.progression = progression.music21_progression_from_numerals(pre_progression.split('-'))
        temp.rhythmic_style = int(rhythmic_style)
        temp.m.makeMeasures(inPlace=True)
        temp.calculate_all_characteristics()
        temp.m.insert(0,instrument.Flute())
        melodies.append(temp)
    return melodies

def get_n_random_melodies(n, sort_by):
    melodies = []
    if isinstance(progression.GLOBAL_ROOT, type(None)):
        progression.GLOBAL_ROOT = progression.std_initialization()
    for i in range(n):
        melody = create_random_melody()
        melody.progression = progression.music21_progression_from_numerals(progression.create_progression(progression.GLOBAL_ROOT, 0.2))
        melody.calculate_all_characteristics()
        melodies.append(melody)
    sorted_melodies = []
    if sort_by == 'energy':
        sorted_melodies = sorted(melodies, key=lambda melody:melody.energy)
    elif sort_by == 'progression_dissonance':
        sorted_melodies = sorted(melodies, key=lambda melody:melody.progression_dissonance)
    elif sort_by == 'key_dissonance':
        sorted_melodies = sorted(melodies, key=lambda melody:melody.key_dissonance)
    elif sort_by == 'rhythmic':
        sorted_melodies = sorted(melodies, key=lambda melody:melody.rhythmic)
    else:
        sorted_melodies = melodies
    return sorted_melodies
