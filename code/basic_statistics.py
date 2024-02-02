import pickle
import pathlib
import music21
import matplotlib.pyplot as plt

music21_scores_path = pathlib.Path('data/music21/palestrina_scores.pkl')
music21_scores_file = open(music21_scores_path, 'rb')
palestrina_scores = pickle.load(music21_scores_file)

plt.hist([score.duration.quarterLength for score in palestrina_scores], bins=100)
plt.show()
