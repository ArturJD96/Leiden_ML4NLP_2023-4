import pathlib
import numpy
import matplotlib.cm as cmx
import matplotlib.pyplot as plt
import matplotlib
from sklearn.decomposition import PCA
import mpld3 # mouse hovering

PARTS = 3

scores = numpy.load(f'data/{PARTS}_parts/score_vectors.npy').swapaxes(0,1)
labels = pathlib.Path(f'data/{PARTS}_parts/labels.txt').read_text().split('\n')

fig, ax = plt.subplots(1)

# 2-D

# pca_2d = PCA(n_components=2)
# pca_2d.fit_transform(scores)
# points_2d = pca_2d.components_

# ax = plt.subplot()
# ax.set_title("PCA of vectorized beginnings of Palestrina mass scores.", size=10)
# scatter_2d = ax.scatter(points_2d[0], points_2d[1])

# tooltip = mpld3.plugins.PointLabelTooltip(scatter_2d, labels=labels)
# mpld3.plugins.connect(fig, tooltip)

# mpld3.show()

# 3-D

pca_3d = PCA(n_components=4)
pca_3d.fit_transform(scores)
points_3d = pca_3d.components_


cm = plt.get_cmap('jet')
cNorm = matplotlib.colors.Normalize(vmin=min(points_3d[3]), vmax=max(points_3d[3]))
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
c = scalarMap.to_rgba(points_3d[3])
scalarMap.set_array(points_3d[3])
fig.colorbar(scalarMap, label='Test')

# ax = plt.subplot(projection='3d')
scatter_3d = ax.scatter3D(points_3d[0], points_3d[1], points_3d[2], points_3d[3])

# for i, label in enumerate(labels): #plot each point + it's index as text above
#     ax.scatter(points_3d[0,i], points_3d[1,i], points_3d[2,i], color='b') 
#     ax.text(points_3d[0,i], points_3d[1,i], points_3d[2,i], label.split(": ")[1], size=3, zorder=1, color='k') 

plt.show()