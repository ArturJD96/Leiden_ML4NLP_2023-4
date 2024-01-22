import numpy
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

scores = numpy.load('data/score_vectors.npy')

pca = PCA(n_components=2)
pca.fit_transform(scores)

print(pca.components_)

plt.scatter(pca.components_[0], pca.components_[1])
plt.show()


# plt.figure()
# colors = ["navy", "turquoise", "darkorange"]
# lw = 2

# for color, i, target_name in zip(colors, [0, 1, 2], target_names):
#     plt.scatter(
#         X_r[y == i, 0], X_r[y == i, 1], color=color, alpha=0.8, lw=lw, label=target_name
#     )
# plt.legend(loc="best", shadow=False, scatterpoints=1)
# plt.title("PCA of IRIS dataset")