# CONCEPT-BASED TECHNIQUES FOR "MUSICOLOGIST-FRIENDLY" EXPLANATIONS IN A DEEP MUSIC CLASSIFIER


# Introduction

Explanation.
* Explainability / Interpretability: "the study of techniques that generate a human-understandable explanation of a model’s decision" (p. 876)
* Feature-based vs Concept-based

Concept-based explanation techniques.
* TCAV: _Testing with Concept Activation Vectors_
	1. user themself defines concept by providing examples
	2. user interrogates the system if the concept is relevant (or not) for system's decision.
	* supervised learning
	* can be applied to any systems with hidden layers (including NN).
* _Invertible Concept-based Explanations for CNN Models with Non-negative Concept Activation Vectors_ \[14\]
	1. relevant concepts are automatically produced
	2. those are given to user's interpretation
	3. each concept is presented in form of musical excerpts
	* unsupervised learning
	* requiring networks whose: 
		- hidden layers contain only non-negative values
		- have spatial correlation with the input data
		- satisfied by most Convolutional NN.
* _Post-hoc_ approaches

This Paper (p.877):
- uses _post-hoc_ approach for the first time for musical data
- targets system of Kim & al \[15\]
- uses piano MIDI file input
- definition and creation of musical concept datasets
- dedicated visualisation of unsupervised concepts for symbolic music data
- exploration of the Non-negative Tucker Decomposition (NTD) for the factorisation of hidden layers.
- code: https://github.com/CPJKU/composer_concept


# Related work

Music Information Retrieval (MIR)


# EXPERIMENTAL SETUP

Data:
* dataset: MAESTRO v2.0.0 \[22\]
* MIDI representation
* selection:
	- composers: 13 (at least 16 pieces)
	- removed score files with more than one composer (e.g. arrangments)
	- training: 462 pieces
	- validation: 205 pieces
* for each piece:
	- 90 (random) excerpts of 20s

Composer Classifier:
* Kim et al \[15\] https://arxiv.org/abs/2010.00823
	- results unreproducable
	- removing layer of onset information
	- F1: 0.83
* preprocessing: MIDI excepts -> piano roll
	- time step: 50ms
	- matrix 88 x 400
* model:
	- ResNet-50 Convolutional Neural Network \[25\]
	- trained: Stochastic Gradient Descent
		- momentum (0.9)
		- L2 weight regularisation (0.0001)
		- cross-entropy loss function
		- initial training rate: 0.01
		- scheduling: cosine annealing
* goal:
	- F1: 0.93
	- accuracy: 0.93


# SUPERVISED CONCEPT-BASED EXPLANATIONS

Summary:
* supervised concept-based explainer based on TCAV \[12\]
* defining concepts (manually)
* interrogating classifier: how much a concept influences the results of the classifier?

Musical Concept
* _def:_ "characteristics of a certain group of notes" (p. 877)
* _concept datasets:_ sets of piece having one musical concept in common.

Data (concept datasets):
* 3 concept datasets:
	1. "alberti bass"
	2. "difficult-to-play music"
	3. "contrapuntal texture"
* 10 random datasets
* 30 musical excepts per dataset
* 25s each
* data not used in the training set.

**CAV: Concept Activation Vector v^k_l**
* _k_ - concept
* _l_ - neural network layer
* _x_ - piano roll
* calculation:
	- for _l_, compute activation (layer's output)...
	- ...for every _x_ in concept dataset...
	- ...as well as in random dataset.
* activation:
	- tensor in $(H\times W\times C)$ space
	- _H_ - horizontal
	- _W_ - vertical
	- _C_ - channel
* distinguishing _random_ vs _concept_ layer activation:
	- SVM or logistic regression
	- vector of coefficient = v^k_l (orthogonal to the classification boundary)

How a concept _k_ is relevant to a piece x?
$S_(k,o,l) = \nabla g_(l,o)(f_l(x))\dot v^k_l$
* $S_(k,o,l)$ - conceptual sensitivity
* _o_ - composer
* $f_l(x)$ - activation vector (from NN in to _l_ output)
* $g_(l,o)$ (from _l_ output to NN out)
	- transform $f_l(x)$ to _logit_ for the output class _o_.
	- represents remaining computations after _l_ up to the output)

**Scalar S**:
* conceptual sensitivity 
* "how much the output logits change if we perturb the layer acticvations in the direction of the CAV" (p. 878).
* if positive, _k_ encourages the classification of _x_ as _o_.
* local explanation: how system behaves for a specific input.

**TCAV score**:
* global explanation
* not dependent on specific input
* calculation:
	- multiple pieces belonging to one class
	- ratio of pieces for which S is positive \[12\]

TCAV – Experiment
1. compute CAV for every concept
	* https://captum.ai/api/concept.html
	* separating activations of _concept_ and _random_ with SVM
	* dimensionality reduction
		- cropping all concepts to 20s (middle)
		- padding by adding silence to reach length
2. examine the conceptual sensitivities of validartion data
3. compute TCAV for all pieces by the same composer
	* relative amount of positive conceptual sensitivities over the pieces
	* splitting pieces into non-overlapping 20s segments






