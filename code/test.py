from music21 import *

palestrina_score_paths = corpus.getComposer('palestrina')

for score_path in palestrina_score_paths:

    score = corpus.parse(score_path)

    print(score_path)

    fe = features.jSymbolic.DirectionOfMotionFeature(score)
    feature = fe.extract()

    print(feature.vector)