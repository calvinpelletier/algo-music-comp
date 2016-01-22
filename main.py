# main.py
# Calvin Pelletier
# 1/2/16

import music21
music21.environment.set("musicxmlPath", "/usr/bin/musescore")
music21.environment.set("midiPath", "/usr/bin/timidity")
import progression
import melody
import i_o

GLOBAL_IDS = {}

#melodies = i_o.melodies_from_sample_folder()
#for m in melodies:
#    m.calculate_characteristics()
#    m.print_characteristics()
melodies = melody.create_random_melodies(10000, 'energy')
#m = melody.create_random_melody()
#m.calculate_characteristics()
#m.print_characteristics()
#m.calculate_characteristics()
#m.print_characteristics()
for m in melodies:
    m.print_characteristics()
