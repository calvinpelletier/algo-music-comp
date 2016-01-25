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
import minerva

minerva.run()


"""target = melody.Melody
target.energy = 12.0
target.progression_dissonance = 15.0
target.key_dissonance = 10.0
target.rhythmic = 50.0
target.rhythmically_thematic = 60.0
ancestor = melody.create_random_melody()
ancestor.calculate_characteristics()
ancestor.print_characteristics()
result = melody.genetic_algorithm(target, ancestor, 100, 100)
result.calculate_characteristics()
result.print_characteristics()
r = result.get_music21()
song = music21.stream.Score()
song.insert(r)
song.insert(result.chord_progression.get_music21(result.duration()))
song.show('midi')
song.show()
print(result.chord_progression[0].get_music21())"""

"""melodies = melody.create_random_melodies(10000, 'energy')
#analysis.analyze_characteristics(melodies)
for m in melodies:
    m.print_characteristics()"""

"""melodies = i_o.melodies_from_sample_folder()
for m in melodies:
    m.calculate_characteristics()
    m.print_characteristics()"""
