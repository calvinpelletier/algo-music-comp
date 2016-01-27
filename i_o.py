# i_o.py
# Calvin Pelletier
# 1/20/16

import melody
import progression
import music21
import os
import sys

def melody_from_txt_file(filepath):
    f = open(filepath, 'r')
    ret = melody.Melody()
    majorminor = f.readline().rstrip('\n')
    if majorminor == 'minor' or majorminor == 'Minor':
        ret.minor = True
    ret.rhythmic_style = int(f.readline().rstrip('\n'))
    ret.parse(f.readline().rstrip('\n'))
    ret.chord_progression = progression.Progression(f.readline().rstrip('\n').split('-'))
    ret.ID = os.path.basename(filepath)
    f.close()
    return ret


def melodies_from_sample_folder():
    ret = []
    for filename in os.listdir(os.path.join(sys.path[0], "sample-songs")):
        ret.append(melody_from_txt_file(os.path.join(sys.path[0], "sample-songs", filename)))
    return ret

def save_melody(m, name):
    f = open(os.path.join(sys.path[0], "generated-songs", name), 'w')
    if m.minor:
        f.write("minor\n")
    else:
        f.write("major\n")
    f.write(str(int(m.rhythmic_style)) + '\n')
    f.write(str(m) + '\n')
    f.write(str(m.chord_progression))
    f.close()
