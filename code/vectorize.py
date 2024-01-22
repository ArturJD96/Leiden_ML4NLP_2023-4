import pathlib
import music21
import re
import numpy

SCORES = 0 # when 0, take all
PARTS = 4 # how many 'parts' ('voices' or **kern spines) in a score do we look for (if 0, disregard this condition).
PART_MAX = 8 # highest number of parts ('voices') in the database
OFFSET_MAX = (16 * 8) # first 16 bars, 4 half-notes each [in quarter notes length]

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
for path in palestrina_score_paths:
    try:
        text = path.read_text()
        parts = text.count('**kern')
    except UnicodeDecodeError:
        ...
    else:
        if not PARTS or parts == PARTS:
            score = music21.corpus.parse(path)
            palestrina_scores.append(score)

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
vectors = numpy.zeros((OFFSET_MAX * PART_MAX, len(palestrina_scores)))
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
                vectors[dim, score_id] = midi

numpy.save('data/score_vectors', vectors)

score_labels = [f'{score.metadata.parentTitle} - {path.stem}' for score, path in zip(palestrina_scores, palestrina_score_paths)]

with open('data/labels.txt', 'w') as file:
    file.write('\n'.join(score_labels))