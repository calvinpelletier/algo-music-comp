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
    # CONSTANTS
    E_A = 9.5
    E_B = 8.0
    PD_A = 2.2
    PD_B = 12.7
    KD_A = 16.5
    KD_B = 5.4
    R_A = 16.4
    R_B = 8.8
    RT_A = 63.0
    RT_B = 16.1

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
        self.energy = None # average of intervals divided by durations
        self.progression_dissonance = None
        self.key_dissonance = None
        self.rhythmic = None
        self.rhythmically_thematic = None

    # CHARACTERISTIC FUNCTIONS
    def calculate_characteristics(self):
        self.get_energy()
        self.get_progression_dissonance()
        self.get_key_dissonance()
        self.get_rhythmic()
        self.get_rhythmically_thematic()

    def get_characteristics(self):
        ret = []
        ret.append(self.energy)
        ret.append(self.progression_dissonance)
        ret.append(self.key_dissonance)
        ret.append(self.rhythmic)
        ret.append(self.rhythmically_thematic)
        return ret

    def get_energy(self):
        total = 0.0
        for i in range(len(self.notes) - 1):
            total += abs(note.degree_separation(self.notes[i], self.notes[i+1])) / float(self.notes[i].duration ** 2)
        self.energy = self.E_A * total / float(len(self.notes)) + self.E_B

    def get_progression_dissonance(self):
        total = 0.0
        for i in range(len(self.instants)):
            if isinstance(self.instants[i], note.Note):
                total += self.chord_progression.chord_at(i).dissonance_of_note(self.instants[i]) * self.instants[i].duration
            elif isinstance(self.instants[i], note.Extension):
                if isinstance(self.instants[i].src, note.Note):
                    total += self.chord_progression.chord_at(i).dissonance_of_note(self.instants[i].src) * self.instants[i].src.duration
        self.progression_dissonance = self.PD_A * total / float(len(self.notes)) + self.PD_B

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
        self.key_dissonance = self.KD_A * total / float(len(self.notes)) + self.KD_B

    def get_rhythmically_thematic(self):
        IDENTICAL_BONUS = 1.0
        ONE_OFF_BONUS = 0.3
        TWO_OFF_BONUS = 0.1
        measures = []
        total = 0.0
        for i in range(len(self.instants)):
            if i % 8 == 0:
                measures.append([])
            if isinstance(self.instants[i], note.Note):
                measures[i / 8].append(1)
            else:
                measures[i / 8].append(0)
        for i in range(len(measures) - 1):
            for j in range(i + 1, len(measures)):
                count = 0
                for k in range(8):
                    if measures[i][k] != measures[j][k]:
                        count += 1
                if count == 0:
                    total += IDENTICAL_BONUS
                elif count == 1:
                    total += ONE_OFF_BONUS
                elif count == 2:
                    total += TWO_OFF_BONUS
        self.rhythmically_thematic = self.RT_A * total / float(len(measures)) + self.RT_B

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
        self.rhythmic = self.R_A * total / float(len(self.notes)) + self.R_B

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
        if s[0] == '-':
            s = 'x' + s[1:]
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
                try:
                    self.append(note.Note(string=s[old_i:i]))
                except:
                    raise NameError("Tried to create a note from: \'%s\' in string: \'%s\'." % (s[old_i:i], s))

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
        ret.insert(music21.instrument.Piano())
        for note_rest in self.notes_and_rests:
            ret.append(note_rest.get_music21())
        ret.transpose(5, inPlace=True)
        return ret

    def print_characteristics(self):
        print("%s\n%s\nenergy: %f\nprogression dissonance: %f\nkey dissonance: %f\nrhythmic: %f\nrhythmically thematic: %f\n"\
            % (self.ID, str(self), self.energy, self.progression_dissonance,\
            self.key_dissonance, self.rhythmic, self.rhythmically_thematic))

    def distance_to_target(self, target):
        BUFFER = 1.0
        total = 0.0
        characteristics1 = self.get_characteristics()
        characteristics2 = target.get_characteristics()
        for i in range(len(characteristics1)):
            if characteristics2[i] is None:
                continue
            diff = abs(characteristics1[i] - characteristics2[i])
            if diff < BUFFER:
                continue
            total += (diff - BUFFER)**2
        return total

    def mutate(self, in_place=False):
        UPPER_NOTE_BOUND = note.Note(string='5,5')
        LOWER_NOTE_BOUND = note.Note(string='5,3')
        CHANCE_OF_ALTERING = 0.1
        CHANCE_OF_REST = 0.05
        CHANCE_OF_EXTENSION = 0.35
        CHANCE_OF_NOTE = 0.6
        #                      -7    -6    -5    -4    -3    -2     -1    0    +1    +2    +3    +4    +5    +6    +7
        CHANCE_OF_MOVEMENT = [0.00, 0.00, 0.05, 0.05, 0.10, 0.10, 0.15, 0.10, 0.15, 0.10, 0.10, 0.05, 0.05, 0.00, 0.00]

        #seed()
        new_instants = self.instants
        last_note = None
        string = ''
        for instant in new_instants:
            if isinstance(instant, note.Note):
                last_note = note.Note(degree=instant.degree, octave=instant.octave)
            if random() < CHANCE_OF_ALTERING:
                rand = random()
                if rand < CHANCE_OF_REST:
                    instant = note.Rest()
                elif rand < CHANCE_OF_REST + CHANCE_OF_EXTENSION:
                    instant = note.Extension(None)
                else:
                    if isinstance(instant, note.Rest) or isinstance(instant, note.Extension):
                        if last_note is None:
                            last_note = note.Note(string='1,4')
                        instant = note.Note(degree=last_note.degree, octave=last_note.octave)
                    while True:
                        rand = random()
                        i = 0
                        while rand > CHANCE_OF_MOVEMENT[i]:
                            rand -= CHANCE_OF_MOVEMENT[i]
                            i += 1
                        new_instant = instant.transpose(i - 7, in_place=False)
                        if new_instant > LOWER_NOTE_BOUND and new_instant < UPPER_NOTE_BOUND:
                            break
                    instant = new_instant
            if isinstance(instant, note.Note):
                string += str(instant.degree) + ',' + str(instant.octave)
            elif isinstance(instant, note.Rest):
                string += 'x'
            elif isinstance(instant, note.Extension):
                string += '-'
            else:
                raise NameError("Something went horribly wrong.")
        if in_place:
            self.parse(string)
        else:
            ret = Melody(chord_progression=self.chord_progression, minor=self.minor, rhythmic_style=self.minor)
            ret.ID = self.ID
            ret.parse(string)
            return ret

def genetic_algorithm(target, ancestor, generations, num_offspring):
    if ancestor is None:
        parent = create_random_melody()
        parent.calculate_characteristics()
    else:
        parent = ancestor
    for i in range(generations):
        best = parent
        children = []
        for j in range(num_offspring):
            children.append(parent.mutate())
            children[-1].calculate_characteristics()
            if best.distance_to_target(target) > children[-1].distance_to_target(target):
                best = children[-1]
        parent = best
        children = []
    return parent

def create_random_melody(measures=4, chord_progression=progression.Progression(['I', 'V', 'vi', 'IV'])):
    MAX_RANGE = 13 # in degrees
    UPPER_NOTE_BOUND = note.Note(string='5,5')
    LOWER_NOTE_BOUND = note.Note(string='5,3')
    POSSIBLE_START_NOTES = ['1,4', '2,4', '3,4', '4,4', '5,4', '6,4', '7,4', '1,5']
    CHANCE_OF_REST = 0.1
    CHANCE_OF_EXTENSION = 0.5
    MINOR_CHANCE = 0.5
    #                      -7    -6    -5    -4    -3    -2     -1    0    +1    +2    +3    +4    +5    +6    +7
    CHANCE_OF_MOVEMENT = [0.05, 0.05, 0.05, 0.05, 0.05, 0.10, 0.10, 0.10, 0.10, 0.10, 0.05, 0.05, 0.05, 0.05, 0.05]

    #seed()
    ret = Melody()
    if random() < MINOR_CHANCE:
        ret.minor = True
    length = 8 * measures
    ret.chord_progression = chord_progression

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
        if ret.duration() + cur.duration >= length:
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
