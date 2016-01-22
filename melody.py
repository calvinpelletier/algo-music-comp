# melody.py
# Calvin Pelletier
# 1/1/16

import music21
from random import randint, random, seed
import progression
import note

# melody in string format: x 1,1 - 1,2 - - x x | 3,1
# | is a measure divider, x is a rest, - is a continuation of the previous note, 1,2 is the 1 note (relative to key) in the 2nd octave

# NOTE: EVERYTHING IS HANDLED AS IF IT'S IN THE KEY OF C MAJOR/A MINOR
# IF IT'S IN A MINOR, 1 STILL REPRESENTS C, BUT ITS CHARACTERISTICS ACCOUNT FOR THE DIFFERENCES BETWEEN C MAJOR AND A MINOR

class Melody:
    # INITIALIZATION FUNCTIONS
    def __init__(self, chord_progression=progression.Progression(['I', 'V', 'vi', 'IV']), minor=False, rhythmic_style=0):
        self.ID = "unidentified"

        # MELODY
        self.instants = []
        self.notes = []
        self.notes_and_rests = []

        # HELPER INFORMATION
        self.chord_progression = chord_progression
        self.minor = minor
        self.rhythmic_style = rhythmic_style

        # CHARACTERISTICS
        self.energy = 0.0 # average of intervals divided by durations
        self.rhythmic = 0.0
        self.progression_dissonance = 0.0
        self.key_dissonance = 0.0

    # CHARACTERISTIC FUNCTIONS
    def calculate_characteristics(self):
        self.get_energy()
        self.get_progression_dissonance()
        self.get_key_dissonance()
        self.get_rhythmic()

    def get_energy(self):
        total = 0.0
        for i in range(len(self.notes) - 1):
            total += abs(note.degree_separation(self.notes[i], self.notes[i+1])) / float(self.notes[i+1].location - self.notes[i].location)
        self.energy = total / float(len(self.notes))

    def get_progression_dissonance(self):
        total = 0.0
        for i in range(len(self.instants)):
            if isinstance(self.instants[i], note.Note):
                total += self.chord_progression.chord_at(i).dissonance_of_note(self.instants[i]) * self.instants[i].duration
            elif isinstance(self.instants[i], note.Extension):
                if isinstance(self.instants[i].src, note.Note):
                    total += self.chord_progression.chord_at(i).dissonance_of_note(self.instants[i].src) * self.instants[i].src.duration
        self.progression_dissonance = total / float(len(self.notes))

    def get_key_dissonance(self):
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

    def get_rhythmic(self):
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
        for i in range(note_rest.duration - 1):
            extension = note.Extension(note_rest)
            extension.location = len(self.instants)
            self.instants.append(extension)

    def parse(self, string):
        s = string.translate(None, '|')
        s = s.translate(None, ' ')
        self.instants = []
        self.notes = []
        self.notes_and_rests = []
        i = 0
        while i < len(s):
            if s[i] == 'x':
                duration = 1
                i += 1
                while True:
                    if i >= len(s):
                        break
                    if s[i] != '-' and s[i] != 'x':
                        break
                    duration += 1
                    i += 1
                self.append(note.Rest(duration))
            else:
                old_i = i
                i += 3
                while True:
                    if i >= len(s):
                        break
                    if s[i] != '-':
                        break
                    i += 1
                self.append(note.Note(string=s[old_i:i]))

    def __str__(self):
        ret = ''
        for note_rest in self.notes_and_rests:
            if isinstance(note_rest, note.Rest):
                ret += 'x' * note_rest.duration
            else:
                ret += str(note_rest.degree) + ',' + str(note_rest.octave)
                ret += '-' * (note_rest.duration - 1)
        return ret

    def get_music21(self):
        ret = music21.stream.Part()
        for note_rest in self.notes_and_rests:
            ret.append(note_rest.get_music21())
        return ret

    def print_characteristics(self):
        print("%s\n%s\nenergy: %f\nprogression dissonance: %f\nkey dissonance: %f\nrhythmic: %f\n"\
            % (self.ID, str(self), self.energy, self.progression_dissonance, self.key_dissonance, self.rhythmic))

def create_random_melody():
    MAX_RANGE = 13 # in degrees
    UPPER_NOTE_BOUND = note.Note(string='5,5')
    LOWER_NOTE_BOUND = note.Note(string='5,3')
    UPPER_LEN_BOUND = 16 # in measures
    LOWER_LEN_BOUND = 4
    POSSIBLE_START_NOTES = ['1,4', '2,4', '3,4', '4,4', '5,4', '6,4', '7,4', '1,5']
    CHANCE_OF_REST = 0.1
    CHANCE_OF_EXTENSION = 0.5
    MINOR_CHANCE = 0.5
    #                      -7    -6    -5    -4    -3    -2     -1    0    +1    +2    +3    +4    +5    +6    +7
    CHANCE_OF_MOVEMENT = [0.05, 0.05, 0.05, 0.05, 0.05, 0.10, 0.10, 0.10, 0.10, 0.10, 0.05, 0.05, 0.05, 0.05, 0.05]

    seed()
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
            upper_bound = min(UPPER_NOTE_BOUND, lowest_note.transpose(MAX_RANGE, in_place=False))
            lower_bound = max(LOWER_NOTE_BOUND, highest_note.transpose(MAX_RANGE * -1, in_place=False))
            while True:
                cur = note.Note(exact_degree=ret.notes[-1].exact_degree)
                rand = random()
                i = 0
                while rand > CHANCE_OF_MOVEMENT[i]:
                    rand -= CHANCE_OF_MOVEMENT[i]
                    i += 1
                cur.transpose(i - 7)
                if cur < upper_bound and cur > lower_bound:
                    break
            if cur < lowest_note:
                lowest_note = cur
            if cur > highest_note:
                highest_note = cur
        while random() < CHANCE_OF_EXTENSION:
            cur.duration += 1
        if ret.duration() + cur.duration > length:
            cur.duration = length - ret.duration()
            ret.append(cur)
            break
        ret.append(cur)

    return ret

def create_random_melodies(n, sort_by):
    melodies = []
    for i in range(n):
        melodies.append(create_random_melody())
        melodies[-1].calculate_characteristics()
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
