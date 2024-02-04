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


## CAV: Concept Activation Vector v^k_l

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


## Experiment

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
	* 10 runs with 10 random dataset
4. validation
	* two-sided t-test
	* Bonferroni correction
	* significance threshold $\alpha = 0.05/n$
		- _n_ - hypothesis tests (3 + 10)


## Results

* both intuitive and counter-intuitive classifications (table p. 879)
* negative activation should be treated with care.


# Unsupervised concept-based explanations

NN must be:
* convolutional
* use non-negative activation function (e.g. ReLU)

Defining a _concept_:
* layer activations: ${\mathcal{X} = f_l(x_1),...,f_l(x_N)}$
* pieces: $x_l...,x_N$
* _Concept_ defined from clustering layer activations of a (short Euclidean distance).

Disentangling concepts:
* the approach above works best with only _one_ defined concept
* ...however we expect the whole number of concepts!
* concepts can overlap
* use Non-negative Tucker Decomposition (NTD)

## CAV -> Channel-CAV

_Explanation_
* ...given layer actications $f_l(x)$...
* vectors obtained by fixing an index for _W_ and _H_ dimenions (_h_, _w_) \[33\]
* _Channel-mode tubes:_
	- different representation of the same piece with a different _receptive field_ \[34\].
	- represents a piece
* advantages:
	- _dimensionality reduction:_ analyzing channel-mode tubes $\in \mathbb{R}$ **instead** of full layer activations $\in \mathbb{R}^(H\times W\times C)$. \[14\]
	- increasing amount of data
	- highlighting in which part of a piece a certain concept is present

_Computing:_
* dataset: _N_ segments of pieces (20s each)
1. Input each excerpt to the trained system
2. Produce activations for _l_
	* all activations: _tensor_ $\mathcal{X} \in \mathbb{R}^(N\times H\times W\times C$ where:
		- $H$ - frequency
		- $W$ - time
		- $C$ - channel size
3. Applying NTD to $\mathcal{X}$ -> set of C-CAVs.

_Visualisation_ (**piano roll!**)
* "layer activations have a spatial correlation with input data" (p.880) \[35\]
* projecting $h$ and $w$ of each C-CAV to *piano roll*.


## Non-negative Tucker Decomposition

* details: \[33\]
* implementation: \[36\]
	- updating factor matrices: Hierarchical non-negative Alternating Least Squares algorithm
	- updating the core: Fast Iterative Shrinkage-Thresholding Algorithm

Decomposing tensor to:
* non-negative _core_ tensor:
	- $\mathcal{T}\in \mathbb{R}^{N'\times H'\times W'\times C'}$
* multiple _factor_ matrices (one for every dimension \[33\])
	- $\mathcbf{A}\in \mathbb{R}^{N\times N'}$
	- $\mathcbf{B}\in \mathbb{R}^{H\times H'}$
	- $\mathcbf{D}\in \mathbb{R}^{W\times W'}$
	- $\mathcbf{E}\in \mathbb{R}^{C\times C'}$
* $\mathcal{X} \approx \displaystyle\sum_{n=1}^{N'} \displaystyle\sum_{h=1}^{H'} \displaystyle\sum_{w=1}^{W'} \displaystyle\sum_{c=1}^{C'} t_{nhwc}a_n\circ b_h\circ d_w\circ e_c$
	- $t_{nhwc}$ - scalar element
	- $a_n$, $b_h$, $d_w$, $e_c$ - matrices
	- $\circ$ - vector outer product of the column vectors of 4 matrices

Hyperparameters
* $N'$, $H'$, $W'$, $C'$
* numbers of columns of the factor matrices (NTD ranks)
* set as low as possible (decreasing the size of the matrices)

Obtaining C-CAVs:
* "every channel-mode tube in $\mathcal{X}$ can be reconstructed as a weighted sum of the columns of matrix $\mathcbf{E}$ (p.880)
* columns of $\mathbb{E}$ - disentangled C-CAVs.
* ranks $C'$ - number of columns

**Fidelity**: ratio of the predictions remaining unchaged after performing NTD.
* reconstructing original tensor (layer activations)
* "computing output of the composer classifier by feeding it back into the network" (p. 880)


# Experiments

1. Computing unsupervised explanations (for penultimate layer)
2. Testing multiple NTD ranks]

## User concept presentation

"The presentation of piece excerpts is more challenging for musical data than for im- ages" (p.880)

* concept examples
	- positive: 5 piece excerpts (highest average concept presence)
	- negative: 5 piece excerpts (lowest average concept presence)
* Plotly - visual piano roll
* concept presence heatmap (mask over piano roll)
	- slider for heatmap threshold
* simplifying choice to two "contrasting" composers (why one was chosen and not the other?) for psychological reasons (easier to understand for a human why one was chosen but not the other; this gets confusing whith higher number of composers)

Tested factorization approaches:
1. NTD on 4-D matrix
2. NTD on 3-D matrix
	- horizontal \& vertical concatenated
3. NMF on 2-D matrix (as in \[14\])

## Results

1. With 2 composers considered, maximum _fidelity_ is approximated by only 3-5 C-CAVs.
2. No advantage for any factorization techniques when number of C-CAVs is fixed
3. NTD allows for up to 15 times higher compression (of $\mathcal{X}$ with the same fidelity)
4. NTD is much slower to compute
5. Unsupervised explainer gives useful examples for opposing concepts

Issues with non-negative factorisation techniques:
- giving one C-CAV comprising two different concepts
- producing two C-CAV referring to the same concept
- hard to name some C-CAVs


# Conclusions \& Future Work

Supervised explainer:
- useful for testing concept but...
- creating concept dataset is time-consuming,
- requires music expertise,
- trying different concepts to find relevant one,
- ...solved by unsupervised learning

Unsupervised explainer:
- concepts presented with examples

## Future work

Supervise explainer:
- integrating recent promising results
- stricter hypothesis testing

Unsupervised explainer:
- formal user-based evaluation by musicologists
- which number of C-CAVs gives most interpretable musical concepts
- is agreement on naming possible
- attenuating non-negative factorisation problems with sparsity constraints applied to the core tensor and matrices in the NTD

General:
- make excerpt length variable
- longer excerpts can lead to the analysis of the whole structure
- possibility to apply both approaches to audio classifiers
- dedicated user interfaces.




