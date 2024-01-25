import numpy as np
import pathlib
from sklearn.model_selection import train_test_split

# Load the data
data_score = np.load('data/4_parts/score_vectors.npy')
data_labels = pathlib.Path('data/4_parts/labels.txt').read_text().splitlines()

# #Check if score has the same length with labels
# if len(data_score) != len(data_labels):
#     raise ValueError("Number of samples in score vectors and labels are inconsistent.")

# Split the data into 60% training and 40% test
train_data, test_data, train_labels, test_labels = train_test_split(data_score, data_labels, test_size=0.3, random_state=42)

# Print the shapes of the resulting arrays
print("Training data shape:", train_data.shape)
print("Test data shape:", test_data.shape)
print("Training labels length:", len(train_labels))
print("Test labels length:", len(test_labels))

# Save the arrays into separate files
np.save('data/4_parts/train_data.npy', train_data)
np.save('data/4_parts/test_data.npy', test_data)

# Save the labels into separate files
with open('data/4_parts/train_labels.txt', 'w') as file:
    file.write('\n'.join(train_labels))

with open('data/4_parts/test_labels.txt', 'w') as file:
    file.write('\n'.join(test_labels))