import pathlib
import music21
import re

import pickle
import matplotlib.pyplot as plt

# option = {}
SCORES = 0 # when 0, take all
PARTS = 0 # how many 'parts' ('voices' or **kern spines) in a score do we look for (if 0, disregard this condition).
PART_MAX = 8 # highest number of parts ('voices') in the database

VALID_SCORES = 1208
SCORES = SCORES or VALID_SCORES

music21.defaults.ticksPerQuarter = 4

'''
    Get paths to Palestrina files (in 'kern/humdrum' .krn format)
'''
'''
    Get all the scores.
'''

# smallest_duration = 24

def get_scores(paths:list[pathlib.Path]):

    palestrina_scores = []

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

    return palestrina_scores



file_with_pickled_music21_scores = None
palestrina_scores = []
pickled_scores_music21_dir = pathlib.Path('data/music21/palestrina_scores.pkl')

palestrina_score_paths:list[pathlib.PosixPath] = music21.corpus.getComposer('palestrina')[:SCORES]

while not file_with_pickled_music21_scores:

    try:

        file_with_pickled_music21_scores = open(pickled_scores_music21_dir, 'rb')
        palestrina_scores = pickle.load(file_with_pickled_music21_scores)

        if len(palestrina_scores) != SCORES:
            raise FileNotFoundError("The already compiled .pkl file does not have requested metadata and needs to be recompiled")

    except FileNotFoundError:

        print('Parsing **kern humdrum files to music21 format (might take a while)...')
        palestrina_scores = get_scores(palestrina_score_paths)
        pickle.dump(palestrina_scores, open(pickled_scores_music21_dir, 'wb'))


print('Scores:', len(palestrina_scores))
labels = []
for score in palestrina_scores:
    label = score.metadata.getCustom('label')
    label = str(label[0]) if type(label) is tuple else label
    labels.append(label)

'''
    Save all the scores as midi
'''
for i, score in enumerate(palestrina_scores):
    score.flatten().write('midi', fp=f'data/midi/{labels[i]}.midi')