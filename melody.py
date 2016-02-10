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
    # CONSTANTS FOR NORMALIZING CHARACTERISTICS
    EN_A = 8.5
    EN_B = 6.0
    PD_A = 2.2
    PD_B = 12.7
    KD_A = 16.5
    KD_B = 5.4
    RH_A = 46.4
    RH_B = 4.8
    RT_A = 90.0
    RT_B = 16.1
    TT_A = 35.0
    TT_B = 17.0
    RE_A = 21.0
    RE_B = 0.0
    DE_A = 43.0
    DE_B = 0.0
    SI_A = 50.0
    SI_B = 15.0

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
        self.characteristics = {}
        self.characteristics['en'] = None
        self.characteristics['pd'] = None
        self.characteristics['kd'] = None
        self.characteristics['rh'] = None
        self.characteristics['rt'] = None
        self.characteristics['tt'] = None
        self.characteristics['re'] = None
        self.characteristics['de'] = None
        self.characteristics['si'] = None

    # CHARACTERISTIC FUNCTIONS
    def calculate_characteristics(self):
        self.get_energetic()
        self.get_progression_dissonant()
        self.get_key_dissonant()
        self.get_rhythmic()
        self.get_rhythmically_thematic()
        self.get_tonally_thematic()
        self.get_repetitive()
        self.get_dense()
        self.get_silent()

    def get_energetic(self):
        total = 0.0
        for i in range(len(self.notes) - 1):
            total += abs(note.degree_separation(self.notes[i], self.notes[i+1])) / float(self.notes[i].duration)
        if len(self.notes) == 0:
            self.characteristics['en'] = 0.0
        else:
            self.characteristics['en'] = self.EN_A * total / float(len(self.notes)) + self.EN_B

    def get_progression_dissonant(self):
        total = 0.0
        for i in range(len(self.instants)):
            if isinstance(self.instants[i], note.Note):
                total += self.chord_progression.chord_at(i).dissonance_of_note(self.instants[i]) * self.instants[i].duration
            elif isinstance(self.instants[i], note.Extension):
                if isinstance(self.instants[i].src, note.Note):
                    total += self.chord_progression.chord_at(i).dissonance_of_note(self.instants[i].src) * self.instants[i].src.duration
        if len(self.notes) == 0:
            self.characteristics['pd'] = 0.0
        else:
            self.characteristics['pd'] = self.PD_A * total / float(len(self.notes)) + self.PD_B

    def get_key_dissonant(self):
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
        if len(self.notes) == 0:
            self.characteristics['kd'] = 0.0
        else:
            self.characteristics['kd'] = self.KD_A * total / float(len(self.notes)) + self.KD_B

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
        self.characteristics['rh'] = self.RH_A * total / float(self.duration()) + self.RH_B

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
        self.characteristics['rt'] = self.RT_A * total / float(len(measures)) + self.RT_B

    def get_tonally_thematic(self):
        total = 0.0
        sequences = {}
        notes = []
        for n in self.notes:
            notes.append(n.name_with_octave)
        for i in range(len(notes) - 1):
            for j in range(i + 2, len(notes) + 1):
                sequence = '-'.join(notes[i:j])
                if sequences.has_key(sequence):
                    sequences[sequence] += 1
                else:
                    sequences[sequence] = 1
        for key, value in sequences.iteritems():
            if value > 1:
                if len(set(key.split('-'))) != 1:
                    total += float(value)
        if len(self.notes) == 0:
            self.characteristics['tt'] = 0.0
        else:
            self.characteristics['tt'] = self.TT_A * total / float(len(self.notes)) + self.TT_B

    # wrote this when I was way too tired so it's pretty sloppy
    # TODO: rewrite
    def get_repetitive(self):
        IDENTICAL = 15.0
        NON_IDENTICAL = 5.0
        total = 0.0
        measures = []
        for i in range(len(self.instants)):
            if i % 8 == 0:
                measures.append([])
            if isinstance(self.instants[i], note.Note):
                measures[i / 8].append(self.instants[i].degree_octave_str)
            elif isinstance(self.instants[i], note.Extension):
                if isinstance(self.instants[i].src, note.Note):
                    measures[i / 8].append(self.instants[i].src.degree_octave_str + '-')
                else:
                    measures[i / 8].append('x')
            else:
                measures[i / 8].append('x')
        for i in range(len(measures) - 1):
            for j in range(i + 1, len(measures)):
                count = 0
                for k in range(8):
                    if measures[i][k] != measures[j][k]:
                        count += 1
                if count == 0:
                    total += IDENTICAL
                else:
                    total += NON_IDENTICAL / float(count)
        self.characteristics['re'] = self.RE_A * total / float(len(measures)) + self.RE_B


    def get_dense(self):
        self.characteristics['de'] = self.DE_A * len(self.notes) / float(self.duration()) + self.DE_B

    def get_silent(self):
        total = 0
        rest = True
        for instant in self.instants:
            if isinstance(instant, note.Rest):
                total += 1
                rest = True
            elif isinstance(instant, note.Extension):
                if rest:
                    total += 1
            else:
                rest = False
        self.characteristics['si'] = self.SI_A * total / float(self.duration()) + self.SI_B

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
                ret += ' '
            else:
                ret += str(note_rest.degree) + ',' + str(note_rest.octave)
                ret += '-' * (note_rest.duration - 1)
                ret += ' '
        return ret

    def get_music21(self, repeat=2):
        m = music21.stream.Part()
        m.insert(music21.instrument.Piano())
        for i in range(repeat):
            for note_rest in self.notes_and_rests:
                m.append(note_rest.get_music21())
        m.transpose(5, inPlace=True)
        p = self.chord_progression.get_music21(self.duration() * 2)
        ret = music21.stream.Score()
        ret.insert(m)
        ret.insert(p)
        return ret

    def print_characteristics(self):
        print("%s\n%s" % (self.ID, str(self)))
        for key, value in self.characteristics.iteritems():
            print("%s: %f" % (key, value))

    def distance_to_target(self, target):
        total = 0.0
        for key, value in self.characteristics.iteritems():
            if target.characteristics[key] is None:
                continue
            if target.characteristics[key][0] > target.characteristics[key][1]:
                raise NameError("Wrong ordering of target bounds.")
            if value >= target.characteristics[key][0] and value <= target.characteristics[key][1]:
                continue
            if value < target.characteristics[key][0]:
                total += (target.characteristics[key][0] - value)**2
            else:
                total += (value - target.characteristics[key][1])**2
        return total

    def mutate(self, in_place=False):
        UPPER_NOTE_BOUND = note.Note(string='5,5')
        LOWER_NOTE_BOUND = note.Note(string='5,3')
        CHANCE_OF_ALTERING = 0.2
        CHANCE_OF_REST = 0.05
        CHANCE_OF_EXTENSION = 0.55
        CHANCE_OF_NOTE = 0.4
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
            ret = Melody(chord_progression=self.chord_progression, minor=self.minor, rhythmic_style=self.rhythmic_style)
            ret.ID = self.ID
            ret.parse(string)
            return ret

# each characteristic should either be None or a range in form [LOWER_BOUND, UPPER_BOUND]
class Target:
    def __init__(self, en=None, pd=None, kd=None, rh=None, rt=None, tt=None, re=None, de=None, si=None):
        self.characteristics = {}
        self.characteristics['en'] = en
        self.characteristics['pd'] = pd
        self.characteristics['kd'] = kd
        self.characteristics['rh'] = rh
        self.characteristics['rt'] = rt
        self.characteristics['tt'] = tt
        self.characteristics['re'] = re
        self.characteristics['de'] = de
        self.characteristics['si'] = si

def genetic_algorithm(target, ancestor, generations, num_offspring):
    if ancestor is None:
        parent = create_random_melody()
        parent.calculate_characteristics()
    else:
        parent = ancestor
    if generations == 0 or num_offspring == 0:
        return parent
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

def create_random_melodies(n, sort_by='none'):
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
