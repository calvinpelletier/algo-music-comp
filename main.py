# main.py
# Calvin Pelletier
# 1/2/16

import music21
music21.environment.set("musicxmlPath", "/usr/bin/musescore")
music21.environment.set("midiPath", "/usr/bin/timidity")
import progression
import melody
import i_o
import analysis

target = melody.Melody
target.energy = 10.0
target.progression_dissonance = 15.0
target.key_dissonance = 15.0
target.rhythmic = 35.0
ancestor = melody.create_random_melody()
ancestor.calculate_characteristics()
ancestor.print_characteristics()
result = melody.genetic_algorithm(target, ancestor, 100, 100)
result.calculate_characteristics()
result.print_characteristics()
r = result.get_music21()
r.show('midi')
r.show()

#melodies = melody.create_random_melodies(10000, 'none')
#analysis.analyze_characteristics(melodies)

#melodies = i_o.melodies_from_sample_folder()
#for m in melodies:
#    m.calculate_characteristics()
#    m.print_characteristics()
