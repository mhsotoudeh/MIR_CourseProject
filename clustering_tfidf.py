import csv

from sklearn.feature_extraction.text import TfidfVectorizer

from yellowbrick.cluster import KElbowVisualizer
from sklearn.decomposition import TruncatedSVD
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


docs = pd.read_csv('data/raw/phase3_data.csv', encoding='latin1')
print(docs.head())
nrm_docs = []
for text in docs['Text'].tolist():
    tokenized_text = nrm.normalize_english(text)
    nrm_text = ''
    for token in tokenized_text:
        nrm_text += token + ' '
    nrm_docs.append(nrm_text)

vectorizer = TfidfVectorizer()
doc_term_mat = vectorizer.fit_transform(nrm_docs)
pc = TruncatedSVD(n_components=2).fit_transform(doc_term_mat)
pc_1000 = TruncatedSVD(n_components=1000).fit_transform(doc_term_mat)
fig, ax = plt.subplots(3, sharex=True, sharey=True)
fig.set_size_inches(8, 24)

print('*** K-Means ***')

# determining number of clusters
# visualizer = KElbowVisualizer(KMeans(), k=(2, 21))
# visualizer.fit(pc_1000)
# visualizer.show()

N = 11

kmeans = KMeans(n_clusters=N)
kmeans.fit(pc_1000)
targets = kmeans.labels_

with open('kmeans-tfidf.csv', 'w') as outfile:
    csv_writer = csv.writer(outfile, dialect='excel', delimiter=',')
    csv_writer.writerows([["ID", "Cluster"]])
    csv_writer.writerows([[docs["ID"].tolist()[i], targets[i]] for i in range(len(targets))])

# *** visualisation ***
ax[0].set_facecolor('xkcd:sky blue')
ax[0].set_xlabel('PC 1', fontsize=15)
ax[0].set_ylabel('PC 2', fontsize=15)
ax[0].set_title('KMeans', fontsize=20)
ax[0].scatter(pc[:, 0], pc[:, 1], c=targets)

print('*** Hierarchical ***')

# determining number of clusters
# dists = pdist(pc_1000)
# linked = linkage(dists, 'ward')
# labels = range(1, doc_term_mat.shape[0] + 1)
# plt.figure(figsize=(75, 10))
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index')
# plt.ylabel('distance')
# dnd = dendrogram(linked,
#                  orientation='top',
#                  labels=labels,
#                  distance_sort='descending',
#                  show_leaf_counts=True,
#                  truncate_mode='lastp', p=10)
# plt.show()

N = 7

hier = AgglomerativeClustering(n_clusters=N)
hier.fit(pc_1000)
targets = hier.labels_

with open('hierarchical-tfidf.csv', 'w') as outfile:
    csv_writer = csv.writer(outfile, dialect='excel', delimiter=',')
    csv_writer.writerows([["ID", "Cluster"]])
    csv_writer.writerows([[docs["ID"].tolist()[i], targets[i]] for i in range(len(targets))])

# *** visualisation ***
ax[1].set_facecolor('xkcd:sky blue')
ax[1].set_xlabel('PC 1', fontsize=15)
ax[1].set_ylabel('PC 2', fontsize=15)
ax[1].set_title('Hierarchical', fontsize=20)
ax[1].scatter(pc[:, 0], pc[:, 1], c=targets)

print('*** GMM ***')

# using number of clusters from hierarchical
N = 7

gmm = Gmm(6, n_init=2)
gmm.fit(pc_1000)
targets = gmm.predict(pc_1000)

with open('gmm-tfidf.csv', 'w') as outfile:
    csv_writer = csv.writer(outfile, dialect='excel', delimiter=',')
    csv_writer.writerows([["ID", "Cluster"]])
    csv_writer.writerows([[docs["ID"].tolist()[i], targets[i]] for i in range(len(targets))])

# *** visualisation ***
ax[2].set_facecolor('xkcd:sky blue')
ax[2].set_xlabel('PC 1', fontsize=15)
ax[2].set_ylabel('PC 2', fontsize=15)
ax[2].set_title('GMM', fontsize=20)
ax[2].scatter(pc[:, 0], pc[:, 1], c=targets)

plt.show()
