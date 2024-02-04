import pickle
import pathlib
import music21
import matplotlib.pyplot as plt

music21_scores_path = pathlib.Path('data/music21/palestrina_scores.pkl')
music21_scores_file = open(music21_scores_path, 'rb')
palestrina_scores = pickle.load(music21_scores_file)
<<<<<<< HEAD
<<<<<<< HEAD
=======

plt.hist([score.duration.quarterLength for score in palestrina_scores], bins=100)
plt.show()
>>>>>>> ad9e273fe9ae84b8eba0bf2de8ca1a440b1a6f12

plt.hist([score.duration.quarterLength for score in palestrina_scores], bins=100)
plt.show()
=======

plt.hist([score.duration.quarterLength for score in palestrina_scores], bins=100)
plt.show()

>>>>>>> ad9e273fe9ae84b8eba0bf2de8ca1a440b1a6f12
