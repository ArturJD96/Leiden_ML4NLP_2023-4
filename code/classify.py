import pathlib
import numpy as np
import matplotlib.pyplot as plt
import json
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.metrics import classification_report
# from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# import numpy
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA

# scores = np.load('data/4_parts/score_vectors.npy')

# with open('data/MacKay_presentation_types.json', 'r') as file:
#     presentation_types = json.load(file)

data_dir = pathlib.Path('data/4_parts/')

with open(f'{data_dir.__str__()}/labels_annotated.json', 'r') as file:
    presentation_types = list(json.load(file).values())

scores_sliced = np.load(data_dir/'score_vectors.npy')[:len(presentation_types)]

# with open(f'data/MacKay_presentation_types', 'r') as file:
#     presentation_types = json.load(file)

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(scores_sliced, presentation_types, test_size=0.1, random_state=18)

# # Get the common classes between y_train and y_test
# common_classes = list(set(y_train).intersection(y_test))

# # Filter the data based on common classes
# X_train_filtered = [score for score, label in zip(X_train, y_train) if label in common_classes]
# y_train_filtered = [label for label in y_train if label in common_classes]
# X_test_filtered = [score for score, label in zip(X_test, y_test) if label in common_classes]
# y_test_filtered = [label for label in y_test if label in common_classes]

# # Initialize and train the KNeighborsClassifier
# knn_classifier = KNeighborsClassifier(n_neighbors=1)
# knn_classifier.fit(X_train_filtered, y_train_filtered)

# # Make predictions and evaluate accuracy
# predictions = knn_classifier.predict(X_test_filtered)
# accuracy = accuracy_score(y_test_filtered, predictions)

# print(f'Accuracy: {accuracy:.2f}')

X_train, X_test, y_train, y_test = train_test_split(scores_sliced, presentation_types, test_size=0.2, random_state=42)

knn_classifier = KNeighborsClassifier(n_neighbors=1) # arbitrary number
knn_classifier.fit(X_train, y_train)
predictions = knn_classifier.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f'Accuracy: {accuracy:.2f}')

report = classification_report(y_test, predictions)
print("Classification Report:")
print(report)

# print("True Label\tPredicted Label")
# for true_label, predicted_label in zip(y_test, predictions):
#     print(f'{true_label}\t\t{predicted_label}')

# disp = DecisionBoundaryDisplay.from_estimator(knn_classifier, X_test)
# plt.scatter(disp)

# print(labels)

#n_clusters = 10
#kmeans = KMeans(n_clusters=n_clusters, random_state=42)
#kmeans.fit(scores)
#cluster_labels = kmeans.labels_
#print("Cluster Labels:", cluster_labels)