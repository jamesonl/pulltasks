# Experimental, still under development!

import numpy as np
from sklearn.neighbors import NearestNeighbors
samples = [[0, 0, 2], [1, 0, 0], [0, 0, 1], [0, 1, 1], [1, 1, 1], [10, 10, 19]]

neigh = NearestNeighbors(n_neighbors=5, radius=0.4)
neigh.fit(samples)

print(neigh.kneighbors_graph([[10, 1, 10]]))
