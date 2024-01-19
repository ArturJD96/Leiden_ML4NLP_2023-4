import pathlib
import music21
import re
import numpy

SCORES = 10 # when 0, take all
# PARTS = 4 # how many 'parts' ('voices' or **kern spines) in a score do we look for.
PART_MAX = 8
OFFSET_MAX = (16 * 8) # first 16 bars, 4 half-notes each [in quarter notes length]


'''
    Get paths to Palestrina files (in 'kern/humdrum' .krn format)
'''
palestrina_score_paths:list[pathlib.PosixPath] = music21.corpus.getComposer('palestrina') # FIRST 10 !!!
# print(f'All Palestrina file scores: {len(palestrina_score_paths)}')

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
        score = music21.corpus.parse(path)
        palestrina_scores.append(score)
        # if parts == PARTS:
        #     score = music21.corpus.parse(path)
        #     palestrina_scores.append(score)

# print(f'All Palestrina {PARTS}-part scores: {len(palestrina_scores)}')

'''
    Get vectorized result as a 3-dimensional numpy array, where:
    'x' is score id
    'y' is the current offset
    'z' are the (vertical) pitches in this offset (by part id.)
'''
vectors = numpy.zeros((SCORES, OFFSET_MAX, PART_MAX))
for score_id, score in enumerate(palestrina_scores):
    for part_id, part in enumerate(score.parts):
        part_flat = part.flatten()
        midi = 0
        for offset in range(OFFSET_MAX):
            noteOrRest = part_flat.getElementsByOffset(offset).notesAndRests
            for n in noteOrRest:
                midi = 0 if n.isRest else (n.pitch.midi / 127)
            vectors[score_id, offset, part_id] = midi
    
print(vectors)