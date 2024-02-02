# Leiden_ML4NLP_2023-4
Final project for the course Machine Learning for NLP with prof. Raaijmakers, Leiden 2023/4

Google Drive: https://drive.google.com/drive/folders/1mMV4X_hmfVgMZUVkpMOSdv-SM2QyDCMD?usp=sharing

What we want to achieve:
Language model (expert system) that describes, from a given excerpt from the Palestrina score, occuring clausulae.

Prerequisites to process the data:
Compatible only with Python 3.7
- miditoolkit 1.0.1
- numpy 1.21.6
- madmom
- chorder 0.1.4
- scikit-learn 1.0.2

Else it's run on Python 3.12

Prerequsites to train the data:
- torch 1.3.1
- torchvision 0.4.2
- pytorch-fast-transformers
- miditoolkit 1.0.1

Run those scripts:
python3.12 code/midify.py;
python3.7 make-corpus/midi2corpus.py;
python3.7 make-corpus/corpus2events.py;
python3.7 make-corpus/events2words;
python3.7 make-corpus/compile.py;
