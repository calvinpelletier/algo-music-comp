# melody.py
# Calvin Pelletier
# 1/1/16

from random import randint
import progression

# melody in string format: x 1,1 - 1,2 - - x x 3,1
# x is a rest, - is a continuation of the previous note, 1,2 is the 1 note (relative to key) in the 2nd octave
# melody in int array format: 0 is -, -1 is x, 1 is 1,1, 8 is 1,2

class Melody:
    energy = 0.0
    progression = []
    progression_dissonance = 0.0
    key_dissonance = 0.0
    rhythmic = 0.0
    def __init__(self, str_melody, arr_melody, minor, rhythmic_style):
        self.str_melody = str_melody
        self.arr_melody = arr_melody
        self.minor = minor
        self.rhythmic_style = rhythmic_style

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
    for i in range(length):
        if i == 0:
            note = randint(LOWER_START_NOTE_BOUND, UPPER_START_NOTE_BOUND)
            arr_melody.append(note)
            str_melody += exact_note_to_note_octave(note)
            prev_note = note
            min_note = note
            max_note = note
        else:
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
    return Melody(str_melody, arr_melody, randint(0, 100) / 100.0 < MINOR_CHANCE, 0)

# average of intervals divided by durations
# high means sporatic melody
def energy(arr_melody):
    num_notes = 0
    total = 0
    duration = -1
    last_note = -1
    for instant in arr_melody:
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
    total += (abs(last_note - instant) + 1) / float(duration)
    return total / float(len(arr_melody))
    # return total / float(num_notes)

# average of notes being within/not within the chord progression times the duration
# high means dissonant melody
def progression_dissonance(arr_melody, chord_progression):
    INSTANTS_PER_CHORD = 8
    instants_per_progression = INSTANTS_PER_CHORD * len(chord_progression)
    num_notes = 0
    total = 0
    i = 0
    while i < len(arr_melody):
        if arr_melody[i] == 0 or arr_melody[i] == -1:
            i += 1
        else:
            num_notes += 1
            note = (arr_melody[i] - 1) % 7 + 1
            chord = chord_progression[(i % instants_per_progression) / INSTANTS_PER_CHORD]
            duration = 1
            i += 1
            while i < len(arr_melody):
                if arr_melody[i] == 0:
                    if chord != chord_progression[(i % instants_per_progression) / INSTANTS_PER_CHORD]:
                        if not progression.note_in_chord(note, chord):
                            total += duration
                        chord = chord_progression[(i % instants_per_progression) / INSTANTS_PER_CHORD]
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
    return total / float(num_notes)

def key_dissonance(arr_melody, minor):
    # favors 1 and 5 primarily, then the pentatonic scale
    #                    1    2    3    4    5    6    7
    DISSONANCE_MAJOR = [0.0, 0.4, 0.4, 0.7, 0.2, 0.4, 1.0]
    DISSONANCE_MINOR = [0.4, 0.4, 0.2, 0.7, 0.4, 0.0, 1.0]

    num_notes = 0
    total = 0
    i = 0
    while i < len(arr_melody):
        if arr_melody[i] == 0 or arr_melody[i] == -1:
            i += 1
        else:
            num_notes += 1
            note = (arr_melody[i] - 1) % 7 + 1
            if minor:
                dissonance = DISSONANCE_MINOR[note - 1]
            else:
                dissonance = DISSONANCE_MAJOR[note - 1]
            duration = 1
            i += 1
            while i < len(arr_melody):
                if arr_melody[i] == 0:
                    i += 1
                    duration += 1
                else:
                    break
            total += dissonance * duration
    # return total / float(len(arr_melody))
    return total / float(num_notes)

# amount of repetition in the melody
#def thematic(melody):

# amount of notes placed on the strong beats, weighted by their duration.
def rhythmic(arr_melody, style):
    #                       1   and   2   and   3   and   4   and
    RHYTHMIC_STYLE = []
    RHYTHMIC_STYLE.append([1.0, 0.0, 0.5, 0.0, 1.0, 0.0, 0.5, 0.0]) # style 0
    RHYTHMIC_STYLE.append([0.0, 1.0, 0.0, 0.5, 0.0, 1.0, 0.0, 0.5]) # style 1
    RHYTHMIC_STYLE.append([0.5, 0.0, 1.0, 0.0, 0.5, 0.0, 1.0, 0.0]) # style 2
    RHYTHMIC_STYLE.append([0.0, 0.5, 0.0, 1.0, 0.0, 5.0, 0.0, 1.0]) # style 3

    num_notes = 0
    total = 0
    i = 0
    while i < len(arr_melody):
        if arr_melody[i] == 0 or arr_melody[i] == -1:
            i += 1
        else:
            num_notes += 1
            strength = RHYTHMIC_STYLE[style][i % 8]
            duration = 1
            i += 1
            while i < len(arr_melody):
                if arr_melody[i] == 0:
                    i += 1
                    duration += 1
                else:
                    break
            total += strength * duration
    # return total / float(len(arr_melody))
    return total / float(num_notes)

#def rhythmic_variation(melody):

#def tonal_variation(melody):

# returns int array
def array_from_string(melody):
    ret = []
    i = 0
    while i < len(melody):
        if melody[i] == ' ':
            i += 1
        elif melody[i] == 'x':
            ret.append(-1)
            i += 2
        elif melody[i] == '-':
            ret.append(0)
            i += 2
        else:
            ret.append(note_octave_to_exact_note(int(melody[i]), int(melody[i+2])))
            i += 4
    return ret

def note_octave_to_exact_note(note, octave):
    return note + 7 * (octave - 1)

# returns in str format: 1,4
def exact_note_to_note_octave(note):
    octave = (note - 1) / 7 + 1
    note_in_octave = (note - 1) % 7 + 1
    return str(note_in_octave) + ',' + str(octave)

def print_examples():
    dict = {}
    # 100 Years by Five for Fighting
    one_hundred_years = "x 1,5 - 1,5 - 3,4 - 4,4 - - 4,4 3,4 4,4 5,4 x x x x 1,5 1,5 - 3,4 - 4,4 - - 4,4 3,4 4,4 5,4 4,4 3,4 - 1,5 - 1,5 - 5,4 - 3,4 - - x x 3,4 4,4 5,4 6,4 - - x 3,4 3,4 3,4 - 3,4 - 2,4 x x x x x x"
    dict['one_hundred_years'] = Melody(one_hundred_years, array_from_string(one_hundred_years), False, 1)
    dict['one_hundred_years'].progression = ['I', 'IV', 'ii', 'V', 'I', 'vi', 'ii', 'IV']
    # Test
    test = "1,4 1,4 - - x x 1,4 - - - - - - - - - 1,4 x x x x x x 1,4 - 1,4 - 1,4 - - 1,4 - -"
    dict['test'] = Melody(test, array_from_string(test), False, 0)
    dict['test'].progression = ['I', 'I']
    for key in dict:
        print("%s: %s\nprogression: %s\nenergy: %f\nprogression_dissonance: %f\nkey_dissonance: %f\nrhythmic: %f\n" % (key, dict[key].str_melody, '-'.join(dict[key].progression), energy(dict[key].arr_melody), progression_dissonance(dict[key].arr_melody, dict[key].progression), key_dissonance(dict[key].arr_melody, dict[key].minor), rhythmic(dict[key].arr_melody, dict[key].rhythmic_style)))

def print_n_random_melodies(n, sort_by):
    melodies = []
    root = progression.std_initialization()
    for i in range(n):
        melody = create_random_melody(64)
        melody.progression = progression.create_progression(root, 0.2)
        melody.energy = energy(melody.arr_melody)
        melody.progression_dissonance = progression_dissonance(melody.arr_melody, melody.progression)
        melody.key_dissonance = key_dissonance(melody.arr_melody, melody.progression)
        melody.rhythmic = rhythmic(melody.arr_melody, melody.rhythmic_style)
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
        print("random: %s\nprogression: %s\nenergy: %f\nprogression_dissonance: %f\nkey_dissonance: %f\nrhythmic: %f\n" % (melody.str_melody, '-'.join(melody.progression), melody.energy, melody.progression_dissonance, melody.key_dissonance, melody.rhythmic))
