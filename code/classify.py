import pathlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.inspection import DecisionBoundaryDisplay
# from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# import numpy
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA

scores = np.load('data/score_vectors.npy')
labels = pathlib.Path('data/labels.txt').read_text().split('\n')

# pca = PCA(n_components=2)
# pca.fit_transform(scores)

scaler = StandardScaler()
scores_standardized = scaler.fit_transform(scores)

X_train, X_test, y_train, y_test = train_test_split(scores_standardized, labels, test_size=0.2, random_state=42)

knn_classifier = KNeighborsClassifier(n_neighbors=5, metric='euclidean') # arbitrary number
knn_classifier.fit(X_train, y_train)
predictions = knn_classifier.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy:.2f}')

print(predictions)

# disp = DecisionBoundaryDisplay.from_estimator(knn_classifier, X_test)
# plt.scatter(disp)

# print(labels)

#n_clusters = 10
#kmeans = KMeans(n_clusters=n_clusters, random_state=42)
#kmeans.fit(scores)
#cluster_labels = kmeans.labels_
#print("Cluster Labels:", cluster_labels)