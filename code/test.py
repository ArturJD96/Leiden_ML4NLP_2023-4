import music21

palestrina_corpus = music21.corpus.getComposer('Palestrina')

score = music21.corpus.parse(palestrina_corpus[0])

print(score)