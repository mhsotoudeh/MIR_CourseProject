import csv

from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from yellowbrick.cluster import KElbowVisualizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from scipy.spatial.distance import pdist

from sklearn.mixture import GaussianMixture as Gmm
from matplotlib.patches import Ellipse
from sklearn import metrics

import Phase_1__Part_1_Normalization as nrm

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

docs = pd.read_csv('data/raw/phase3_data.csv', encoding='latin1')
print(docs.head())
nrm_docs = []
for text in docs['Text'].tolist():
    tokenized_text = nrm.normalize_english(text)
    nrm_docs.append(tokenized_text)

final_docs = [TaggedDocument(doc, [i]) for i, doc in enumerate(nrm_docs)]

model = Doc2Vec(final_docs, vector_size=5, window=2, min_count=1, workers=4)
word2vec_mat = np.array([model.infer_vector(d) for d in nrm_docs])

pc = PCA(n_components=2).fit_transform(word2vec_mat)
fig, ax = plt.subplots(3, sharex=True, sharey=True)

print('*** K-Means ***')

# determining number of clusters
# visualizer = KElbowVisualizer(KMeans(), k=(2, 21))
# visualizer.fit(word2vec_mat)
# visualizer.show()

N = 6

kmeans = KMeans(n_clusters=N)
kmeans.fit(word2vec_mat)
targets = kmeans.labels_

with open('kmeans-w2v.csv', 'w') as outfile:
    csv_writer = csv.writer(outfile, dialect='excel', delimiter=',')
    csv_writer.writerows([["ID", "Cluster"]])
    csv_writer.writerows([[docs["ID"].tolist()[i], targets[i]] for i in range(len(targets))])

# *** visualisation ***
ax[0].set_facecolor('xkcd:cyan')
ax[0].set_xlabel('PC 1', fontsize=15)
ax[0].set_ylabel('PC 2', fontsize=15)
ax[0].set_title('KMeans', fontsize=20)
ax[0].scatter(pc[:, 0], pc[:, 1], c=targets)


print('*** Hierarchical ***')

# determining number of clusters
# dists = pdist(word2vec_mat)
# print(len(dists))
# linked = linkage(dists, 'single')
# labels = range(1, word2vec_mat.shape[0] + 1)
# plt.figure(figsize=(75, 10))
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index')
# plt.ylabel('distance')
# dnd = dendrogram(linked,
#                  orientation='top',
#                  labels=labels,
#                  distance_sort='descending',
#                  show_leaf_counts=True,
#                  truncate_mode='level', p=30)
# plt.show()

N = 2

hier = AgglomerativeClustering(n_clusters=N)
hier.fit(word2vec_mat)
targets = hier.labels_

with open('hierarchical-w2v.csv', 'w') as outfile:
    csv_writer = csv.writer(outfile, dialect='excel', delimiter=',')
    csv_writer.writerows([["ID", "Cluster"]])
    csv_writer.writerows([[docs["ID"].tolist()[i], targets[i]] for i in range(len(targets))])

# *** visualisation ***
ax[1].set_facecolor('xkcd:cyan')
ax[1].set_xlabel('PC 1', fontsize=15)
ax[1].set_ylabel('PC 2', fontsize=15)
ax[1].set_title('Hierarchical', fontsize=20)
ax[1].scatter(pc[:, 0], pc[:, 1], c=targets)

print('*** GMM ***')

# using number of clusters from hierarchical
N = 2

gmm = Gmm(N, n_init=2)
gmm.fit(word2vec_mat)
targets = gmm.predict(word2vec_mat)

with open('gmm-w2v.csv', 'w') as outfile:
    csv_writer = csv.writer(outfile, dialect='excel', delimiter=',')
    csv_writer.writerows([["ID", "Cluster"]])
    csv_writer.writerows([[docs["ID"].tolist()[i], targets[i]] for i in range(len(targets))])

# *** visualisation ***
ax[2].set_facecolor('xkcd:cyan')
ax[2].set_xlabel('PC 1', fontsize=15)
ax[2].set_ylabel('PC 2', fontsize=15)
ax[2].set_title('GMM', fontsize=20)
ax[2].scatter(pc[:, 0], pc[:, 1], c=targets)

plt.show()
