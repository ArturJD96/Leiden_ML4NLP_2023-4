import pathlib
import music21
import re

import pickle
import matplotlib.pyplot as plt

# option = {}
SCORES = 0 # when 0, take all
PARTS = 0 # how many 'parts' ('voices' or **kern spines) in a score do we look for (if 0, disregard this condition).
PART_MAX = 8 # highest number of parts ('voices') in the database
OFFSET_MAX = 408 # [in quarter notes length]. Note: smallest has 24; longest has 1776

VALID_SCORES = 1243
SCORES = SCORES or VALID_SCORES

music21.defaults.ticksPerQuarter = 4
data_path = pathlib.Path('data/')

'''
    Get paths to Palestrina files (in 'kern/humdrum' .krn format)
'''

# smallest_duration = 24

def get_metadata(scores):

    return f'''
This file was extracted
using vectorize.py
following settings:

SCORES: {scores or SCORES}
PARTS: {'all' if not PARTS else PARTS}
OFFSET_MAX: {OFFSET_MAX}
'''


def get_scores(paths:list[pathlib.Path]):

    palestrina_scores = []
    labels = []

    for i, path in enumerate(paths):

        try:
            text = path.read_text()
            parts = text.count('**kern')
        except UnicodeDecodeError:
            path = paths[:i] + paths[i+1:]
        else:
            if parts <= PART_MAX and not PARTS or parts == PARTS:

                # add score
                score = music21.corpus.parse(path)
                palestrina_scores.append(score)

                # add score label
                mass_name = score.metadata.parentTitle
                part_name = pathlib.Path(score.metadata.filePath).stem
                label = f'{mass_name}: {part_name}'
                score.metadata.addCustom('label', label)
                labels.append(label)

    return palestrina_scores, labels

'''
    Save:
    - scores to data/music21
    - 
'''

file_with_pickled_music21_scores = None
palestrina_scores = []
labels = []
pickled_scores_music21_dir = data_path / 'music21/palestrina_scores.pkl'
palestrina_score_paths:list[pathlib.PosixPath] = music21.corpus.getComposer('palestrina')[:SCORES]

dumped = False

while not file_with_pickled_music21_scores:
    try:
        file_with_pickled_music21_scores = open(pickled_scores_music21_dir, 'rb')
        palestrina_scores = pickle.load(file_with_pickled_music21_scores)
        labels = (data_path / 'music21/labels.txt').read_text().splitlines()
        if not dumped or len(palestrina_scores) != SCORES:
            raise FileNotFoundError("The already compiled .pkl file does not have requested metadata and needs to be recompiled")
    except FileNotFoundError:
        print('Parsing **kern humdrum files to music21 format (might take a while)...')
        palestrina_scores, labels = get_scores(palestrina_score_paths)
        pickle.dump(palestrina_scores, open(pickled_scores_music21_dir, 'wb'))
        dumped = True

print('Scores:', len(palestrina_scores))
labels = []
for score in palestrina_scores:
    label = score.metadata.getCustom('label')
    label = str(label[0]) if type(label) is tuple else label
    labels.append(label)

'''
    Crop scores by the (quarterNoteLenght) offset
'''
croped_scores = [score.flatten().getElementsByOffset(0, OFFSET_MAX, includeEndBoundary=False).stream() for score in palestrina_scores]

'''
    Save all the scores as midi
'''
for score, label in zip(croped_scores, labels):
    # merge all ties BEFORE!!!
    score.write('midi', fp=f'data/midi/{label}.midi')

'''
    Save label file as txt
'''
(data_path / 'music21/labels.txt').write_text('\n'.join(labels))

'''
    Save metadata file
'''
metadata = get_metadata(len(croped_scores))
(data_path / 'music21/metadata.txt').write_text(metadata)