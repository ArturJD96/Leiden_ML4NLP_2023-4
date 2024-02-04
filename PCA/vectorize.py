import pathlib
import music21
import re
import numpy

import pickle

PARTS = 8
PART_MAX = 8
OFFSET_MAX = 0

print('Reading Palestrina scores from pickle...')
score_pickled_path = pathlib.Path('data/music21/palestrina_scores.pkl')
palestrina_scores = pickle.load(open(score_pickled_path, 'rb'))
palestrina_labels = pathlib.Path('data/music21/labels.txt').read_text.splitlines()
max_length = max([score.duration.quarterLength for score in palestrina_scores])

ai_scores = pathlib.Path('gen_midis').iterdir()
'''
    Get vectorized result as a 3-dimensional numpy array, where:
    'x' is score id
    'y' is the current offset
    'z' are the (vertical) pitches in this offset (by part id.)

    Initialize the array with the following dimensions:
    * SCORES – how many scores from the database are used.
    * OFFSET_MAX – what is the size of window (a grid of quarter notes).
    * PART_MAX - what is the highest number of parts (voices) in a score.
'''




vectors = numpy.zeros((len(palestrina_scores), (OFFSET_MAX * PART_MAX)))
for score_id, score in enumerate(palestrina_scores):
    for offset in range(OFFSET_MAX):
        for part_id, part in enumerate(score.parts):
            if part_id < PART_MAX:
                part_flat = part.flatten()
                midi = 0 # number from 0 to 127
                noteOrRest = part_flat.getElementsByOffset(offset).notesAndRests
                for n in noteOrRest:
                    midi = 0 if n.isRest else (n.pitch.midi / 127)
                # vectors[score_id, offset, part_id] = midi
                dim = part_id + (offset * PART_MAX)
                vectors[score_id, dim] = midi

data_path = pathlib.Path(f"data/{'all' if not PARTS else PARTS}_parts/")
data_path.mkdir(parents=True, exist_ok=True)
numpy.save(data_path / 'score_vectors', vectors)

# score_labels = [f'{score.metadata.parentTitle} - {path.stem}' for score, path in zip(palestrina_scores, palestrina_score_paths)]
(data_path / 'labels.txt').write_text('\n'.join(labels))

metadata = f'''
This file was extracted
using vectorize.py
following settings:

SCORES: {'all' if not SCORES else SCORES}
PARTS: {'all' if not PARTS else PARTS}
OFFSET_MAX: {OFFSET_MAX}
'''
(data_path / 'metadata.txt').write_text(metadata)