import pickle
import pathlib
import music21
import matplotlib.pyplot as plt

### WORKING CODE for getting score lengths

# music21_scores_path = pathlib.Path('data/music21/palestrina_scores.pkl')
# music21_scores_file = open(music21_scores_path, 'rb')
# palestrina_scores = pickle.load(music21_scores_file)

# QUARTER_NOTE_LENGTH = 409
# longer_scores = 0
# shorter_scores = 0
# for score in palestrina_scores:
#     length = score.duration.quarterLength
#     if length <= QUARTER_NOTE_LENGTH:
#         shorter_scores += 1
#     else:
#         longer_scores += 1
# percent_of_shorter_scores = shorter_scores / len(palestrina_scores) * 100
# print(f'{percent_of_shorter_scores}% has length of {QUARTER_NOTE_LENGTH} or less.')

# plt.hist([score.duration.quarterLength for score in palestrina_scores], bins=100)
# plt.show()
### END

palestrina_dir = pathlib.Path('data/midi/')
generated_dir = pathlib.Path('gen_midis/')

def get_corpus_from_midi(path:pathlib.Path):
    return [music21.converter.parse(p) for p in path.iterdir() if p.suffix == '.mid' or p.suffix == '.midi']

corpus = get_corpus_from_midi(palestrina_dir)
# corpus = get_corpus_from_midi(generated_dir)

score = music21.stream.Stream()
for s in corpus:
    score.insert(s)

p = music21.graph.plot.HistogramPitchSpace(score)
p.title = 'Palestrina MIDI Pitch Histogram'
p.run()
p.write('graphs/histogram_palestrina.pgf')