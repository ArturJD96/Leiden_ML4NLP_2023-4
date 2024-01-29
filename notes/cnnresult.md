conv2d - Applies a 2D convolution over an input signal composed of several input planes. - https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html
max_pooling2d - Max pooling operation for 2D spatial data. - https://keras.io/api/layers/pooling_layers/max_pooling2d/
batch_normalization - Layer that normalizes its inputs. Batch normalization applies a transformation that maintains the mean output close to 0 and the output standard deviation close to 1. - https://keras.io/api/layers/normalization_layers/batch_normalization/
flatten - Flattens the input. Does not affect the batch size. - https://keras.io/api/layers/reshaping_layers/flatten/
dense - Just your regular densely-connected NN layer. - https://keras.io/api/layers/core_layers/dense/
dropout - Applies dropout to the input. The Dropout layer randomly sets input units to 0 with a frequency of rate at each step during training time, which helps prevent overfitting. Inputs not set to 0 are scaled up by 1 / (1 - rate) such that the sum over all inputs is unchanged. - https://keras.io/api/layers/regularization_layers/dropout/



Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 conv2d (Conv2D)             (None, 84, 286, 32)       320       
                                                                 
 max_pooling2d (MaxPooling2  (None, 42, 143, 32)       0         
 D)                                                              
                                                                 
 batch_normalization (Batch  (None, 42, 143, 32)       128       
 Normalization)                                                  
                                                                 
 conv2d_1 (Conv2D)           (None, 40, 141, 32)       9248      
                                                                 
 max_pooling2d_1 (MaxPoolin  (None, 20, 71, 32)        0         
 g2D)                                                            
                                                                 
 batch_normalization_1 (Bat  (None, 20, 71, 32)        128       
 chNormalization)                                                
                                                                 
 conv2d_2 (Conv2D)           (None, 19, 70, 32)        4128      
                                                                 
 max_pooling2d_2 (MaxPoolin  (None, 10, 35, 32)        0         
 g2D)                                                            
                                                                 
 batch_normalization_2 (Bat  (None, 10, 35, 32)        128       
 chNormalization)                                                
                                                                 
 flatten (Flatten)           (None, 11200)             0         
                                                                 
 dense (Dense)               (None, 64)                716864    
                                                                 
 dropout (Dropout)           (None, 64)                0         
                                                                 
 dense_1 (Dense)             (None, 10)                650       
                                                                 
=================================================================
Total params: 731594 (2.79 MB)
Trainable params: 731402 (2.79 MB)
Non-trainable params: 192 (768.00 Byte)

