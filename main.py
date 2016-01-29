# main.py
# Calvin Pelletier
# 1/2/16

import music21
music21.environment.set("musicxmlPath", "/usr/bin/musescore")
music21.environment.set("midiPath", "/usr/bin/timidity")
import minerva

minerva.run()
