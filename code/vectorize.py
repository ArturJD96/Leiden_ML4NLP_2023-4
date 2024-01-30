import pathlib
import music21
import re
import numpy

# import pickle # rewrite to store the music21 scores as .pkl files.

SCORES = 0 # when 0, take all
PARTS = 0 # how many 'parts' ('voices' or **kern spines) in a score do we look for (if 0, disregard this condition).
PART_MAX = 8 # highest number of parts ('voices') in the database
# OFFSET_MAX = (9 * 8) # first 9 bars, 4 half-notes each [in quarter notes length]. Note: smallest has 24; longest has 1776
OFFSET_MAX = 1

'''
    Get paths to Palestrina files (in 'kern/humdrum' .krn format)
'''
print('Parsing **kern humdrum files to music21 format (might take a while)...')
palestrina_score_paths:list[pathlib.PosixPath] = music21.corpus.getComposer('palestrina') # FIRST 10 !!!
palestrina_score_paths = palestrina_score_paths[:(SCORES if SCORES else len(palestrina_score_paths))]

'''
    Get all the scores.
'''
palestrina_scores = []
labels = []
smallest_duration = 0

for i, path in enumerate(palestrina_score_paths):

    try:
        text = path.read_text()
        parts = text.count('**kern')
    except UnicodeDecodeError:
        palestrina_score_paths = palestrina_score_paths[:i] + palestrina_score_paths[i+1:]
    else:
        if parts <= PART_MAX and not PARTS or parts == PARTS:

            # add score
            score = music21.corpus.parse(path)
            palestrina_scores.append(score)

            # add score label
            mass_name = score.metadata.parentTitle
            part_name = path.stem
            label = f'{mass_name}: {part_name}'
            labels.append(label)



# print(f'All Palestrina {PARTS}-part scores: {len(palestrina_scores)}')

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
    print(f'Processing score {score_id+1} out of {len(palestrina_scores)}')
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