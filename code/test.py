import pathlib
import music21
import requests

palestrina_score_paths:list[pathlib.PosixPath] = music21.corpus.getComposer('palestrina')
score:music21.stream.base.Score = music21.corpus.parse(palestrina_score_paths[0])
fe:music21.features.jSymbolic.DirectionOfMotionFeature = music21.features.jSymbolic.DirectionOfMotionFeature(score)
feature:music21.features.base.Feature = fe.extract()
print(feature.vector)