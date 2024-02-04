import pathlib
import music21
import requests

import musif

palestrina_score_paths:list[pathlib.PosixPath] = music21.corpus.getComposer('palestrina')
score:music21.stream.base.Score = music21.corpus.parse(palestrina_score_paths[0])
fe:music21.features.jSymbolic.DirectionOfMotionFeature = music21.features.jSymbolic.DirectionOfMotionFeature(score)
feature:music21.features.base.Feature = fe.extract()
print(feature.vector)

# from musif.config import ExtractConfiguration
# from musif.extract.extract import FeaturesExtractor

# musif.extract.constants.MUSIC21_FILE_EXTENSIONS = ['.xml', '.mxl', '.musicxml', '.mid', '.mei', '.krn']

# path = palestrina_score_paths[0].parent

# config = ExtractConfiguration(
#     None,
#     data_dir = path,
#     basic_modules=["scoring"],
#     features = ["core", "ambitus", "melody", "tempo", 
#               "density", "texture", "lyrics", "scale", 
#               "key", "dynamics", "rhythm"],
#     parallel =  -1 #use > 1 if you wish to use parallelization (runs faster, uses more memory)

# )

# extractor = FeaturesExtractor(config)

# df = extractor.extract()
# print('Shape df: ', df.shape)
# df.head()