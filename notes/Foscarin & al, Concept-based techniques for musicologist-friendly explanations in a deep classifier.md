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


