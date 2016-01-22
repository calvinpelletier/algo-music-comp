# note.py
# Calvin Pelletier
# 1/20/16

# key of C major assumed
# degree 1 is C, degree 2 is D, etc. (1-indexed to coincide with modern music theory)
# an eighth note has a duration of 1 tick

# NoteIK class:
#   location:
#       myNote.location
#   init (multiple accepted formats):
#       Note(string="1,5---")
#       Note(exact_degree=34, duration=1)
#       Note(degree=4, octave=3, duration=8)
#   transpose (in place transposition in degrees):
#       myNote.transpose(-3)
#   get_music21_note (returns music21 format):
#       myMusic21Note = myNote.get_music21_note()
#   >, <, >=, <=, ==, != (overloaded comparison operators)
# Rest class:
#   location:
#       myRest.location
#   init (duration in ticks):
#       Rest(4)
# Extension class:
#   location:
#       myExtension.location
#   init (object that this is an extension of):
#       Extension(myNote)
# Other:
#  degree_separation (returns value in degrees, takes two Note objects as input, positive means second note is higher):
#       num = note.degree_separation(myNote, myOtherNote)

import music21

class Note:
    def __init__(self, *args, **kwargs):
        if len(args) != 0:
            raise NameError("Invalid use of NoteIK")
        if kwargs.has_key('string'):
            self.degree = int(kwargs['string'][0])
            self.octave = int(kwargs['string'][2])
            self.duration = len(kwargs['string']) - 2
        elif kwargs.has_key('exact_degree'):
            self.degree = (kwargs['exact_degree'] - 1) % 7 + 1
            self.octave = (kwargs['exact_degree'] - 1) / 7 + 1
            self.duration = kwargs.get('duration', 1)
        elif kwargs.has_key('degree') and kwargs.has_key('octave'):
            self.degree = kwargs['degree']
            self.octave = kwargs['octave']
            self.duration = kwargs.get('duration', 1)
        else:
            raise NameError("Invalid use of Note()")
        self.location = None
        self.on_change()
    # called anytime this note's value changed
    def on_change(self):
        self.exact_degree = self.degree + 7 * (self.octave - 1)
        self.degree_octave_str = str(self.degree) + ',' + str(self.octave)
        self.name = name_from_degree(self.degree)
        self.name_with_octave = self.name + str(self.octave)
    # in scale degrees
    def transpose(self, degrees, in_place=True):
        if in_place:
            self.degree += degrees
            while self.degree < 1:
                self.degree += 7
                self.octave -= 1
            while self.degree > 7:
                self.degree -= 7
                self.octave += 1
            self.on_change()
        else:
            ret = Note(degree=self.degree, octave=self.octave)
            ret.transpose(degrees)
            return ret
    def get_music21(self):
        ret = music21.note.Note(name_from_degree(self.degree) + str(self.octave))
        ret.quarterLength = 0.5 * self.duration
        return ret
    # OVERLOADED OPERATORS
    def __lt__(self, other):
        return self.exact_degree < other.exact_degree
    def ___le__(self, other):
        return self.exact_degree <= other.exact_degree
    def __eq__(self, other):
        return self.exact_degree == other.exact_degree
    def __ne__(self, other):
        return self.exact_degree != other.exact_degree
    def __gt__(self, other):
        return self.exact_degree > other.exact_degree
    def __ge__(self, other):
        return self.exact_degree >= other.exact_degree

class Rest:
    def __init__(self, duration=1):
        self.duration = duration
        self.location = None
    def get_music21(self):
        ret = music21.note.Rest()
        ret.quarterLength = 0.5 * self.duration
        return ret

class Extension:
    def __init__(self, src):
        self.src = src
        self.location = None

def name_from_degree(degree):
    if degree < 1 or degree > 7:
        raise NameError("Invalid degree.")
    names = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    return names[degree - 1]

# positive indications that note2 is higher than note1
def degree_separation(note1, note2):
    return note2.exact_degree - note1.exact_degree
