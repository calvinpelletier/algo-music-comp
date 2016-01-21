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
    notes_and_rests = []

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
        self.notes_and_rests.append(note_rest)
        if isinstance(note_rest, note.Note):
            self.notes.append(note_rest)
        for range(note_rest.duration - 1):
            extension = Extension(note_rest)
            extension.location = len(self.instants)
            self.instants.append(extension)


def create_random_melody():
    MAX_RANGE = 20 # in semitones
    UPPER_NOTE_BOUND = note.Note('5,5')
    LOWER_NOTE_BOUND = note.Note('5,3')
    UPPER_LEN_BOUND = 16 # in measures
    LOWER_LEN_BOUND = 4
    POSSIBLE_START_NOTES = ['1,4', '2,4', '3,4', '4,4', '5,4', '6,4', '7,4', '1,5']
    CHANCE_OF_REST = 0.1
    CHANCE_OF_EXTENSION = 0.4
    MINOR_CHANCE = 0.5

    ret = Melody()
    length = 8 * randint(LOWER_LEN_BOUND, UPPER_LEN_BOUND)
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
