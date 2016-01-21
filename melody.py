# melody.py
# Calvin Pelletier
# 1/1/16

import music21
from random import randint, random
import progression
import note

# melody in string format: x 1,1 - 1,2 - - x x | 3,1
# | is a measure divider, x is a rest, - is a continuation of the previous note, 1,2 is the 1 note (relative to key) in the 2nd octave

# NOTE: EVERYTHING IS HANDLED AS IF IT'S IN THE KEY OF C MAJOR/A MINOR
# IF IT'S IN A MINOR, 1 STILL REPRESENTS C, BUT ITS CHARACTERISTICS ACCOUNT FOR THE DIFFERENCES BETWEEN C MAJOR AND A MINOR

class Melody:
    # MELODY
    ticks = []
    notes = []

    # HELPER INFORMATION
    progression = None
    minor = None
    rhythmic_style = None # see rhythmic()

    # CHARACTERISTICS
    energy = 0.0 # average of intervals divided by durations
    rhythmic = 0.0
    progression_dissonance = 0.0
    key_dissonance = 0.0

    # INITIALIZATION FUNCTIONS
    def __init__(self, progression=progression.Progression(['I', 'V', 'vi', 'IV']), minor=False, rhythmic_style=0):
        self.progression = progression
        self.minor = minor
        self.rhythmic_style = rhythmic_style

    # CHARACTERISTIC FUNCTIONS
    def calculate_all_characteristics(self):
        self.energy()
        self.progression_dissonance()
        self.key_dissonance()
        self.rhythmic()

    def energy(self):
        total = 0.0
        for i in range(len(self.notes) - 1):
            total += abs(note.degree_separation(notes[i], notes[i+1])) / float(notes[i+1].location - notes[i].location)
        self.energy = total / float(len(notes))

    def progression_dissonance(self):
        total = 0.0
        for i in self.instants:
            if isinstance(self.instants[i], note.Note):
                total += self.progression.chord_at(i).dissonance_of_note(self.instants[i].degree) * self.instants[i].duration
            elif isinstance(self.instants[i], note.Extension):
                if isinstance(self.instants[i].src, note.Note):
                    total += self.progression.chord_at(i).dissonance_of_note(self.instants[i].src.degree) * self.instants[i].src.duration
        self.progression_dissonance = total / float(len(self.notes))

    def key_dissonance(self):
        # favors 1 and 5 primarily, then the pentatonic scale
        #                    1    2    3    4    5    6    7
        DISSONANCE_MAJOR = [0.0, 0.4, 0.4, 0.7, 0.2, 0.4, 1.0]
        DISSONANCE_MINOR = [0.4, 0.4, 0.2, 0.7, 0.4, 0.0, 1.0]

        total = 0.0
        for n in self.notes:
            if self.minor:
                total += DISSONANCE_MINOR[n.degree - 1] * n.duration
            else:
                total += DISSONANCE_MAJOR[n.degree - 1] * n.duration
        self.key_dissonance = total / float(len(self.notes))

    #def rhythmically_thematic():

    #def tonally_thematic():

    def rhythmic(self):
        #                       1   and   2   and   3   and   4   and
        RHYTHMIC_STYLE = []
        RHYTHMIC_STYLE.append([1.0, 0.0, 0.5, 0.0, 0.7, 0.0, 0.5, 0.0]) # style 0
        RHYTHMIC_STYLE.append([0.0, 1.0, 0.0, 0.5, 0.0, 0.7, 0.0, 0.5]) # style 1
        RHYTHMIC_STYLE.append([0.5, 0.0, 1.0, 0.0, 0.5, 0.0, 0.7, 0.0]) # style 2
        RHYTHMIC_STYLE.append([0.0, 0.5, 0.0, 1.0, 0.0, 5.0, 0.0, 0.7]) # style 3

        total = 0.0
        for n in self.notes:
            total += RHYTHMIC_STYLE[self.rhythmic_style][n.location % 8] * n.duration
        self.rhythmic = total / float(len(self.notes))

    #def rhythmic_variation():

    #def tonal_variation():

    # OTHER FUNCTIONS
    def duration(self):
        return len(self.instants)

    def append(self, note_rest):
        note_rest.location = len(self.instants)
        self.instants.append(note_rest)
        if isinstance(note_rest, note.Note):
            self.notes.append(note_rest)
        for range(note_rest.duration - 1):
            extension = Extension(note_rest)
            extension.location = len(self.instants)
            self.instants.append(extension)

    # extends last note or rest by one tick
    #def extend_last(self):
    #    i = len(self.instants) - 1
    #    while isinstance(instants[i], note.Extension):
    #        i -= 1
    #    instants[i].duration += 1
    #    if isinstance(self.instants[i], note.Note):
    #        self.notes[-1].duration = instants[i].duration



def create_random_melody():
    MAX_RANGE = 13 # in degrees
    UPPER_NOTE_BOUND = note.Note('5,5')
    LOWER_NOTE_BOUND = note.Note('5,3')
    UPPER_LEN_BOUND = 16 # in measures
    LOWER_LEN_BOUND = 4
    POSSIBLE_START_NOTES = ['1,4', '2,4', '3,4', '4,4', '5,4', '6,4', '7,4', '1,5']
    CHANCE_OF_REST = 0.1
    CHANCE_OF_EXTENSION = 0.5
    MINOR_CHANCE = 0.5
    #                      -7    -6    -5    -4    -3    -2     -1    0    +1    +2    +3    +4    +5    +6    +7
    CHANCE_OF_MOVEMENT = [0.05, 0.05, 0.05, 0.05, 0.05, 0.10, 0.10, 0.10, 0.10, 0.10, 0.05, 0.05, 0.05, 0.05, 0.05]

    ret = Melody()
    if random() < MINOR_CHANCE:
        ret.minor = True
    length = 8 * randint(LOWER_LEN_BOUND, UPPER_LEN_BOUND)

    start_note = note.Note(string=POSSIBLE_START_NOTES[randint(0, len(POSSIBLE_START_NOTES) - 1)])
    while random() < CHANCE_OF_EXTENSION:
        start_note.duration += 1
    ret.append(start_note)
    lowest_note = start_note
    highest_note = start_note
    while True:
        rand = random()
        if rand < CHANCE_OF_REST:
            cur = note.Rest()
        else:
            while True:
                cur = note.Note(exact_degree=ret.notes[-1].exact_degree)
                rand = random()
                i = 0
                while rand > CHANCE_OF_MOVEMENT[i]:
                    rand -= CHANCE_OF_MOVEMENT[i]
                    i += 1
                cur.transpose(i - 7)
                upper_bound = min(UPPER_NOTE_BOUND, lowest_note.transpose(MAX_RANGE, in_place=False))
                lower_bound = max(LOWER_NOTE_BOUND, highest_note.transpose(MAX_RANGE * -1, in_place=False))
                if cur < upper_bound and cur > lower_bound:
                    break
            if cur < lowest_note:
                lowest_note = cur
            if cur > highest_note:
                highest_note = cur
        while random() < CHANCE_OF_EXTENSION:
            cur.duration += 1
        if ret.duration + cur.duration > length:
            cur.duration = length - ret.duration
            ret.append(cur)
            break
        ret.append(cur)

    return ret

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
