'''
FEATURE EXTRACTION AND MACHINE LEARNING
ON SYMBOLIC MUSIC USING THE music21 TOOLKIT

Cuthbert, M. S.
Ariza, Ch.
Friedland, L.

12th International Society for Music Information Retrieval Conference (ISMIR 2011)

# 1. INTRODUCTION

"Most machine learning algo- rithms run on data that can be represented as numbers. While many types of datasets naturally lend themselves to numerical representations, much of the richness of music (especially music expressed in symbolic forms such as scores) resists easily being converted to the numerical forms that enable classification and clustering tasks.
" (p. 387)

Examples of widely used data:
* pitch class
* relative note lengths

Examples of musicological information:
* pitch vs current key
* is note metrically strong or weak
* what text is being sung at the same time
* are chords in open or closed position

Music21 example tasks:
* common framework for various symbolic music formats
  (MusicXML, MuseData, ABC, MIDI, Kern etc.):
  _encoding agnostic_.
* creating sounding score representations
* reducing simultaneities to chords
* analysis of metrical accents

Music21 'features' module:
* adding numerical representations of presence/absence, prevalence etc
* classify by graphical score characteristics

*FEMS* – Feature Extraction Methods


# 2. FEATURE EXTRACTION IN MUSIC21

## 2.1 FE from jSymbolic

jSymbolic by Cory McKay
* part of jMIR toolkit
* for classifying MIDI files

Music21 jSymbolic implementation:
* most of symbolic music formats available
* optimized

Music21 native FEMS
* using advantages of Python's OOP.
* some are expanded jSymbolic (e.g. 'Quality')
* proposed by McKay but not implemented in jSymbolic

Ex 1.: obtaining fraction of ascending notes
'''

import pathlib
import music21
import requests

palestrina_score_paths:list[pathlib.PosixPath] = music21.corpus.getComposer('palestrina')
score:music21.stream.base.Score = music21.corpus.parse(palestrina_score_paths[0])
fe:music21.features.jSymbolic.DirectionOfMotionFeature = music21.features.jSymbolic.DirectionOfMotionFeature(score)
feature:music21.features.base.Feature = fe.extract()
print(feature.vector)


'''
Ex 2.: checking if initial time signature has triple meter
(running on two files: one local, one ONLINE).
'''

# a mass by Palestrina encoded as 4/4
score_local = music21.converter.parse(palestrina_score_paths[1])
feature = music21.features.jSymbolic.TripleMeterFeature(score_local)
print(feature.extract().vector)

# softly-softly by Mark Paul, in 3/4
try:
	score_online = music21.converter.parse("http://static.wikifonia.org/10699/musicxml.xml") # Not working!
	music21.features.setData(score_online)
	print(features.extract().vector)
except requests.exceptions.ConnectionError:
	print("Page does not exist or there is no connection.")

'''
## 2.2 Feature Extractors Native to music21

Typical symbolic music aspects:
* note spellig
* tied notes representation
* correctly vs incorrectly spelled triad in a polyphonic context (IncorrectlySpelledTriadPrevalence)

Notational features not affecting playback:
* scribe's predilection for beaming
* using metadata (e.g. ComposerPopularity)

Ex. 3.: report base-10 logarithm of number of Google hits for a composer's name
'''

score_mozart = music21.corpus.parse('mozart/k155', 2)
print(score_mozart.metadata.composer)
feature:music21.features.native.ComposerPopularity = music21.features.native.ComposerPopularity(score_mozart)
# print(feature.extract().vector) # ???


'''
2.23 Writing Custom Feature Extractors

```._process()```
* sets values of the vector of an internally stored Feature object.

```FeatureExtractor``` superclass
* automatic access to Score presentations:
	- ```.flat``` property (flattening the stream)
	- chord reduction
	- histograms
* ```self.data``` - list of cached representations
* ```self.stream``` - access to the score


Ex. 4.: custom feature extracting musica ficta (non-written accidentals)
'''

'''Feature Extractor definition'''
class MusicaFictaFeature(music21.features.FeatureExtractor):
	
	name = 'Musica Ficta'
	discrete = False
	dimensions = 1
	id = 'mf'

	def _process(self):
		
		all_pitches = self.stream.flat.pitches

		# N.B.: self.data['flat.pitches'] works
		# equally well and caches the result for
		# faster access by other FEMS.
		
		fictaPitches = 0
		for pitch in all_pitches:

			if pitch.name == 'B-':
				continue
			elif pitch.accidental is not None and pitch.accidental.name != 'natural':
				ficta_pitches += 1

			self._feature.vector[0] = ficta_pitches / float(len(all_pitches))

# example of usage of the new method on two pieces # (1) D. Luca early 15th c. Gloria
luca = music21.corpus.parse('luca/gloria.mxl') # file not found
feature = MusicaFictaFeature(luca)
print(feature.extract().vector)

# (2) Monteverdi, late 16th c. madrigal
mv = corpus.parse('monteverdi/madrigal.3.1.xml') # file not found
feature.setData(mv)
print(fe.extract().vector)

'''
# 3. MULTIPLE FEATURE EXTRACTORS AND MULTIPLE SCORES

Music21:
- caches and runs fast many scores
- graphs the results

## 3.1 Extracting Information from DataSets

```DataSet```
* classify group of scores by a class value (using set of FEMS)
* ```.addFeatureExtractors([fems])``` - add FEM
* ```.extractorsById()``` - get FEM by id
	- id 'all' gets all fems
* ```addData()``` - add Music21 Stream to DataSet
	- optionally specify class value, id)
	- accepts file path, URL, corpus reference.

Ex. 5.: run note-length-related FEMS on works by Bach and Handel.
'''

data_set = music21.features.DataSet(classLabel='Composer')
fes:list = music21.features.extractorsById(['ql1','ql2','ql3'])
data_set.addFeatureExtractors(fes)

bach_1 = music21.corpus.parse('bwv1080', 7).measures(0, 50)
data_set.addData(bach_1, classValue='Bach', id='artOfFugue')
data_set.addData('bwv66.6.xml', classValue='Bach')
data_set.addData('c:/handel/hwv56/movement3-05.md', classValue='Handel')
data_set.addData('http://www.midiworld.com/midis/other/handel/gfh-jm01.mid')
data_set.process()

'''
```OutputFormat```
* can be subclassble to develop more writing file formats.

```DataSet``` output:
* ```write(file name/format)``` - save file using OutputFormat object.
	- csv
	- tsv
	- arff (Attribute-Relation File Format)
* ```.getFeaturesAsList()``` -> [[results]]
* ```.getString``` -> Str (data as string)

Visualisation:
* Matplotlib
* music notation (e.g Lilypond)

Ex. 6.: some visualisations.
'''

# a) make comma-separated file
data_set.write('/usr/cuthbert/baroqueQLs.csv')

# b) print attribute labels
print(data_set.getAttributeLabels())

# c) gets feature output
feature_list = data_set.getFeaturesAsList()
print(feature_list[0])

# d) display in OrangeTab [???]
print(music21.features.OutputTabOrange(data_set).getString())

# e) examine feature vectors and display in lilypond
for i in range(len(feature_list)):
	if feature_list[i][2] == 0.5:
		data_set.streams[i].show('lily.png')

# f) plot last two features (most common note length and its prevalence) for each piece
p = graph.PlotFeatures(data_set.streams, fes[1:], roundDigits = 2)
p.process()

'''
## 3.2 Using Feature Data for Classification

Orange
* has GUI
* integrates well with Music21

Weka
* other data mining package


# 4. DEMONSTRATIONS AND RESULTS

Ex. 7.:
* 24 pitch and rhythm feature extractors
* classifying monophonic folksongs as (mostly) German OR Chineese
* two classification methods
	1. MajorityLearner (choose most common classification)
	2. k-nearest neighbor (assigning majority label among k most similar training examples)
* consulting "ground truth"
'''

import orange, orngTree

train_data = orange.ExampleTable('/folkTrain.tab')
test_data  = orange.ExampleTable('/folkTest.tab')

majClassifier = orange.MajorityLearner(train_data)
knnClassifier = orange.kNNLearner(train_data)
majWrong = 0
knnWrong = 0

for testRow in test_data:

  majGuess = majClassifier(testRow)
  knnGuess = knnClassifier(testRow)
  realAnswer = testRow.getclass()

  if majGuess == realAnswer:
    majCorrect += 1

  if knnGuess == realAnswer:
    knnCorrect += 1

total = float(len(test_data))

print(majCorrect/total, knnCorrect/total)

'''
Ex. 8.: Using 10-fold cross-validation
with Weka's variety of classifiers:
* majority (baseline)
* Naive Bayes
* Naive Bayes (using supervised discretization option)
* Decision tree
* Logistic regression
* K-nearest neighbor (k=3)

Results:
* kNN was the best classifier (96%)
* Decision tree is helpful

Ex. 9.: Decision tree on 'Bach vs. Monteverdi'
* 46 works of each composer
* 6 features selected as informative
* 86% accuracy

Prospects:
* choose appropriate playback instrument depending on piece's location
* lowering barriers to use MIR by wide audience

## 5. FUTURE WORK

Proposed problems:
- new extractors
- assign composer names to anonymous
  works of Middle Ages and Renaissance
- popular music genre classification of leadsheets
- change in use of chromatic harmony from XVI to XIX centuries
- explore SVM and clustering algorithms
- audio data as input
- making software for sophisticated musical listening 

 