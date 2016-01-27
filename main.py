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
#import song

minerva.run()


"""target = melody.Melody()
target.energy = 12.0
target.progression_dissonance = 15.0
target.key_dissonance = 10.0
target.rhythmic = 50.0
target.rhythmically_thematic = None
ancestor = melody.create_random_melody()
ancestor.calculate_characteristics()
ancestor.print_characteristics()
result = melody.genetic_algorithm(target, ancestor, 10, 100)
result.calculate_characteristics()
result.print_characteristics()
m = result.get_music21()
song = music21.stream.Score()
song.insert(m)
song.insert(result.chord_progression.get_music21(result.duration()))
hihat = music21.stream.Part()
hihat.insert(music21.instrument.HiHatCymbal())
while m.quarterLength > hihat.quarterLength:
    temp = music21.note.Note(music21.midi.percussion.PercussionMapper().midiInstrumentToPitch(music21.instrument.HiHatCymbal()))
    #temp.storeInstrument = music21.instrument.HiHatCymbal()
    temp.quarterLength = 2.0
    hihat.append(temp)
bass_drum = music21.stream.Part()
bass_drum.insert(music21.instrument.BassDrum())
while m.quarterLength > bass_drum.quarterLength:
    temp = music21.note.Unpitched()
    temp.storeInstrument = music21.instrument.BassDrum()
    temp.quarterLength = 2.0
    bass_drum.append(temp)
snare = music21.stream.Part()
snare.insert(music21.instrument.SnareDrum())
temp = music21.note.Unpitched()
temp.storeInstrument = music21.instrument.SnareDrum()
temp.quarterLength = 2.0
snare.insert(1.0, temp)
while m.quarterLength > snare.quarterLength:
    temp = music21.note.Unpitched()
    temp.storeInstrument = music21.instrument.SnareDrum()
    temp.quarterLength = 2.0
    snare.append(temp)
song.insert(hihat)
song.insert(bass_drum)
song.insert(snare)
song.show('text')
song.show('midi')
#song.show()
"""

"""melodies = melody.create_random_melodies(10000, 'energy')
#analysis.analyze_characteristics(melodies)
for m in melodies:
    m.print_characteristics()"""

"""melodies = i_o.melodies_from_sample_folder()
for m in melodies:
    m.calculate_characteristics()
    m.print_characteristics()"""
