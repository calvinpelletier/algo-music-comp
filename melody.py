# melody.py
# Calvin Pelletier
# 1/1/16

from random import randint

# melody in string format: x 1,1 - 1,2 - - x x 3,1
# x is a rest, - is a continuation of the previous note, 1,2 is the 1 note (relative to key) in the 2nd octave
# melody in int array format: 0 is -, -1 is x, 1 is 1,1, 8 is 1,2

class Melody:
    def __init__(self, str_melody, arr_melody):
        self.str_melody = str_melody
        self.arr_melody = arr_melody

def create_random_melody():
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
    str_melody = ''
    arr_melody = []
    length = randint(32,64)
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
            else if rand < CHANCE_OF_REST + CHANCE_OF_EXTENSION:
                arr_melody.append(0)
                str_melody += ' -'
            else:
                note = randint(max(LOWER_NOTE_BOUND, prev_note - MAX_LEAP, max_note - MAX_RANGE), min(UPPER_NOTE_BOUND, prev_note + MAX_LEAP, min_note + MAX_RANGE))
                min_note = min(min_note, note)
                max_note = max(max_note, note)
                arr_melody.append(note)
                str_melody += ' ' + exact_note_to_note_octave(note)
                prev_note = note
    return Melody(str_melody, arr_melody)

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
    return total / float(num_notes)


# average of notes being within/not within the chord progression divided by the duration
# high means dissonant melody
def dissonance(melody):

# amount of repetition in the melody
def thematic(melody):

# amount of notes placed on the strong beats, weighted by their duration.
def rhythmic(melody):

def rhythmic_variation(melody):

def tonal_variation(melody):

# returns int array
def array_from_string(melody):
    ret = []
    i = 0
    while i < len(melody):
        if melody[i] == ' ':
            i += 1
        else if melody[i] == 'x':
            ret.append(-1)
            i += 2
        else if melody[i] == '-':
            ret.append(0)
            i += 2
        else:
            ret.append(note_octave_to_exact_note(melody[i], melody[i+2]))
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
    one_hundred_years = "x 1,5 - 1,5 - 3,4 - 4,4 - - 4,4 3,4 4,4 5,4 x x x x 1,5 1,5 - 3,4 - 4,4 - - 4,4 3,4 4,4 5,4 4,4 3,4 - 1,5 - 1,5 - 5,4 - 3,4 - - x x 3,4 4,4 5,4 6,4 - - x 3,4 3,4 3,4 - 3,4 - 2,4 x x x x x x"
    dict['one_hundred_years'] = Melody(one_hundred_years, array_from_string(one_hundred_years))
    for key in dict:
        print("%s: %s\nenergy: %d\n", % (key, dict[key].str_melody, energy(dict[key].arr_melody)))

def print_n_random_melodies(n):
    for i in range(n):
        melody = create_random_melody()
        print("random: %s\nenergy: %d\n", % (melody.str_melody, energy(melody.arr_melody)))
