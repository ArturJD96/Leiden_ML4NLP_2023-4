# Leiden_ML4NLP_2023-4
Final project for the course Machine Learning for NLP with prof. Raaijmakers, Leiden 2023/4

Google Drive: https://drive.google.com/drive/folders/1mMV4X_hmfVgMZUVkpMOSdv-SM2QyDCMD?usp=sharing

What we want to achieve:
Using preexisting compound-word-transformer to generate Palestrina score (16th Century)
<<<<<<< HEAD
<<<<<<< HEAD

Research questions:
1. Evaluating how much chord-centered approach results in generation of polyphonic music
2. Asessing NLP methods within the field of generative music: a study on music21 Palestrina database.

System:
- Ubuntu 20.04 via WSL2 (Windows 11)
- Nvidia RTX 3080 TI
- 32 GB RAM
- Driver Version: 471.41
- CUDA Version: 11.4
- CUDA compilation tools release 10.1

Prerequisites to process the data:
Compatible only with Python 3.7
- miditoolkit 1.0.1
- numpy 1.21.6
- madmom
- chorder 0.1.4
- scikit-learn 1.0.2

Else it's run on Python 3.12

Prerequsites to train the data:
- torch 1.7.1+cu110
- pytorch-fast-transformers 0.4.0
- miditoolkit 1.0.1

Run those scripts:
python3.12 code/midify.py;
python3.7 make-corpus/midi2corpus.py;
python3.7 make-corpus/corpus2events.py;
python3.7 make-corpus/events2words.py;
python3.7 make-corpus/compile.py;
<<<<<<< HEAD


Our model/data-preprocess/midi flaws:
- Does not have satisyfing ending
- There's an empty bar in the beginning
- 

EVALUATION:
0. Distance Metrics
1. vector distances [SOURCE?]
    - PCA?
    - Manhattan
2. Human Evaluator?
    - music equivalent to _mean evaluation score_ (MOS) (may not be valid since we're not assessing wav files, but midi)
    - [Kalonaris's HER metric]
    - Musical Turing Test: shorts exerpts are played to human evaluator (3-4 bars) coming from original database and model's output (most likely from the middle). Which is which?
 3. Perplexity?
 
 
=======
>>>>>>> ad9e273fe9ae84b8eba0bf2de8ca1a440b1a6f12
