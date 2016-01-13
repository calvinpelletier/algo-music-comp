# melody.py
# Calvin Pelletier
# 1/1/16

from random import randint
import progression

# melody in string format: x 1,1 - 1,2 - - x x | 3,1
# | is a measure divider, x is a rest, - is a continuation of the previous note, 1,2 is the 1 note (relative to key) in the 2nd octave
# melody in int array format: 0 is -, -1 is x, 1 is 1,1, 8 is 1,2

class Melody:
    # HELPER INFORMATION
    title = "Untitled"
    progression = []
    minor = False
    rhythmic_style = 0 # see rhythmic()

    # CHARACTERISTICS
    energy = 0.0 # average of intervals divided by durations
    rhythmic = 0.0
    progression_dissonance = 0.0
    key_dissonance = 0.0
    thematic = 0.0 # amount of repetition

    # INITIALIZATION FUNCTION
    def __init__(self, str_melody, arr_melody):
        self.str_melody = str_melody
        if len(arr_melody) != 0:
            self.arr_melody = arr_melody
        else:
            self.arr_melody = []
            i = 0
            while i < len(str_melody):
                if str_melody[i] == '|':
                    i += 2
                elif str_melody[i] == 'x':
                    self.arr_melody.append(-1)
                    i += 2
                elif str_melody[i] == '-':
                    self.arr_melody.append(0)
                    i += 2
                elif str_melody[i] >= '0' and str_melody[i] <= '9':
                    if str_melody[i+1] != ',' or str_melody[i+2] < '0' or str_melody[i+2] > '9':
                        raise NameError("Unexpected character when parsing melody")
                    self.arr_melody.append(note_octave_to_exact_note(int(str_melody[i]), int(str_melody[i+2])))
                    i += 4
                else:
                    raise NameError("Unexpected character when parsing melody")

    # CHARACTERISTIC FUNCTIONS
    def calculate_all_characteristics(self):
        self.energy()
        self.progression_dissonance()
        self.key_dissonance()
        self.rhythmic()

    def energy(self):
        num_notes = 0
        total = 0
        duration = -1
        last_note = -1
        for instant in self.arr_melody:
            if last_note == -1:
                if instant == 0 or instant == -1:
                    continue
                last_note = instant
                duration = 1
            if instant != 0 and instant != -1:
                num_notes += 1
                total += (abs(last_note - instant) + 1) / float(duration)
                last_note = instant
                duration = 1
            else:
                duration += 1
        self.energy = total / float(len(self.arr_melody))
        # return total / float(num_notes)

    def progression_dissonance(self):
        if len(self.progression) == 0:
            raise NameError("Tried to calculate progression dissonance without first specifying a progression.")
        INSTANTS_PER_CHORD = 8
        instants_per_progression = INSTANTS_PER_CHORD * len(self.progression)
        num_notes = 0
        total = 0
        i = 0
        while i < len(self.arr_melody):
            if self.arr_melody[i] == 0 or self.arr_melody[i] == -1:
                i += 1
            else:
                num_notes += 1
                note = (self.arr_melody[i] - 1) % 7 + 1
                chord = self.progression[(i % instants_per_progression) / INSTANTS_PER_CHORD]
                duration = 1
                i += 1
                while i < len(self.arr_melody):
                    if self.arr_melody[i] == 0:
                        if chord != self.progression[(i % instants_per_progression) / INSTANTS_PER_CHORD]:
                            if not progression.note_in_chord(note, chord):
                                total += duration
                            chord = self.progression[(i % instants_per_progression) / INSTANTS_PER_CHORD]
                            i += 1
                            duration = 1
                        else:
                            i += 1
                            duration += 1
                    else:
                        break
                if not progression.note_in_chord(note, chord):
                    total += duration
        #return total / float(len(arr_melody))
        self.progression_dissonance = total / float(num_notes)

    def key_dissonance(self):
        # favors 1 and 5 primarily, then the pentatonic scale
        #                    1    2    3    4    5    6    7
        DISSONANCE_MAJOR = [0.0, 0.4, 0.4, 0.7, 0.2, 0.4, 1.0]
        DISSONANCE_MINOR = [0.4, 0.4, 0.2, 0.7, 0.4, 0.0, 1.0]

        num_notes = 0
        total = 0
        i = 0
        while i < len(self.arr_melody):
            if self.arr_melody[i] == 0 or self.arr_melody[i] == -1:
                i += 1
            else:
                num_notes += 1
                note = (self.arr_melody[i] - 1) % 7 + 1
                if self.minor:
                    dissonance = DISSONANCE_MINOR[note - 1]
                else:
                    dissonance = DISSONANCE_MAJOR[note - 1]
                duration = 1
                i += 1
                while i < len(self.arr_melody):
                    if self.arr_melody[i] == 0:
                        i += 1
                        duration += 1
                    else:
                        break
                total += dissonance * duration
        # return total / float(len(arr_melody))
        self.key_dissonance = total / float(num_notes)

    #def thematic(arr_melody):

    def rhythmic(self):
        #                       1   and   2   and   3   and   4   and
        RHYTHMIC_STYLE = []
        RHYTHMIC_STYLE.append([1.0, 0.0, 0.5, 0.0, 1.0, 0.0, 0.5, 0.0]) # style 0
        RHYTHMIC_STYLE.append([0.0, 1.0, 0.0, 0.5, 0.0, 1.0, 0.0, 0.5]) # style 1
        RHYTHMIC_STYLE.append([0.5, 0.0, 1.0, 0.0, 0.5, 0.0, 1.0, 0.0]) # style 2
        RHYTHMIC_STYLE.append([0.0, 0.5, 0.0, 1.0, 0.0, 5.0, 0.0, 1.0]) # style 3

        num_notes = 0
        total = 0
        i = 0
        while i < len(self.arr_melody):
            if self.arr_melody[i] == 0 or self.arr_melody[i] == -1:
                i += 1
            else:
                num_notes += 1
                strength = RHYTHMIC_STYLE[self.rhythmic_style][i % 8]
                duration = 1
                i += 1
                while i < len(self.arr_melody):
                    if self.arr_melody[i] == 0:
                        i += 1
                        duration += 1
                    else:
                        break
                total += strength * duration
        # return total / float(len(arr_melody))
        self.rhythmic = total / float(num_notes)

    #def rhythmic_variation(melody):

    #def tonal_variation(melody):

def note_octave_to_exact_note(note, octave):
    return note + 7 * (octave - 1)

# returns in str format: 1,4
def exact_note_to_note_octave(note):
    octave = (note - 1) / 7 + 1
    note_in_octave = (note - 1) % 7 + 1
    return str(note_in_octave) + ',' + str(octave)

def create_random_melody(length):
    MAX_LEAP = 7
    MAX_RANGE = 11
    UPPER_NOTE_BOUND = 40
    LOWER_NOTE_BOUND = 19
    UPPER_LEN_BOUND = 64
    LOWER_LEN_BOUND = 32
    UPPER_START_NOTE_BOUND = 36
    LOWER_START_NOTE_BOUND = 22
    CHANCE_OF_REST = 0.1
    CHANCE_OF_EXTENSION = 0.4
    MINOR_CHANCE = 0.5

    str_melody = ''
    arr_melody = []
    prev_note = -1
    min_note = -1
    max_note = -1
    count = 0
    for i in range(length):
        if i == 0:
            note = randint(LOWER_START_NOTE_BOUND, UPPER_START_NOTE_BOUND)
            arr_melody.append(note)
            str_melody += exact_note_to_note_octave(note)
            prev_note = note
            min_note = note
            max_note = note
        else:
            if count % 8 == 0:
                str_melody += ' |'
            rand = randint(0, 100) / 100.0
            if rand < CHANCE_OF_REST:
                arr_melody.append(-1)
                str_melody += ' x'
            elif rand < CHANCE_OF_REST + CHANCE_OF_EXTENSION:
                if arr_melody[len(arr_melody) - 1] == -1:
                    arr_melody.append(-1)
                    str_melody += ' x'
                else:
                    arr_melody.append(0)
                    str_melody += ' -'
            else:
                note = randint(max(LOWER_NOTE_BOUND, prev_note - MAX_LEAP, max_note - MAX_RANGE), min(UPPER_NOTE_BOUND, prev_note + MAX_LEAP, min_note + MAX_RANGE))
                min_note = min(min_note, note)
                max_note = max(max_note, note)
                arr_melody.append(note)
                str_melody += ' ' + exact_note_to_note_octave(note)
                prev_note = note
        count += 1
    ret = Melody(str_melody, arr_melody)
    ret.minor = randint(0, 100) / 100.0 < MINOR_CHANCE
    #ret.rhythmic_style =
    return ret

def print_melody(melody):
    print("~~~%s (%s)~~~:\n %s\nenergy: %f\nprogression_dissonance: %f\nkey_dissonance: %f\nrhythmic: %f\n" \
       % (melody.title, '-'.join(melody.progression), melody.str_melody, melody.energy, melody.progression_dissonance, melody.key_dissonance, melody.rhythmic))

def run_test_data():
    melody_data = open('melody_data.txt', 'r')
    while 1:
        title = melody_data.readline().rstrip('\n')
        majorminor = melody_data.readline().rstrip('\n')
        rhythmic_style = melody_data.readline().rstrip('\n')
        melody = melody_data.readline().rstrip('\n')
        progression = melody_data.readline().rstrip('\n')
        if title == '' or majorminor == '' or melody == '' or progression == '':
            break
        temp = Melody(melody, [])
        temp.title = title
        if majorminor == 'major' or majorminor == 'Major':
            temp.minor = False
        elif majorminor == 'minor' or majorminor == 'Minor':
            temp.minor = True
        else:
            raise NameError("Expected result for Major/Minor when parsing melody test data")
        temp.progression = progression.split('-')
        temp.rhythmic_style = int(rhythmic_style)
        temp.calculate_all_characteristics()
        print_melody(temp)

def print_n_random_melodies(n, sort_by):
    melodies = []
    root = progression.std_initialization()
    for i in range(n):
        melody = create_random_melody(64)
        melody.progression = progression.create_progression(root, 0.2)
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
    for melody in sorted_melodies:
        print_melody(melody)
