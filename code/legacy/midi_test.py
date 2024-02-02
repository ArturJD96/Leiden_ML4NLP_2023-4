# from miditoolkit import MidiFile
# from miditoolkit.midi.utils import example_midi_file

import music21
from mido import MidiFile

music21.defaults.ticksPerQuarter = 4

# music21.defaults.ticksPerQuarter

agnus_path = music21.corpus.getComposer("palestrina")[0]
score = music21.corpus.parse(agnus_path)

score.flatten().write('midi', fp=f'test1.midi')
score.flatten().write('midi', fp=f'test2.midi')

m1 = MidiFile('test1.midi')
print(m1.ticks_per_beat)
m2 = MidiFile('test2.midi')
print(m1.ticks_per_beat)


# agnus.plot('pianoroll')

# mf = music21.midi.MidiFile()
# mf.ticksPerQuarterNote = 2
# mf.open(agnus_path)

# print(mf.ticksPerQuarterNote)

# mf.write()
# mf.close()