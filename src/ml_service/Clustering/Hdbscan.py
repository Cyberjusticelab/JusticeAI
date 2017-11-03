from hdbscan import HDBSCAN
from src.ml_service.preprocessing.French.DecisionParse import Parser
from src.ml_service.preprocessing.French.GlobalVariable import Global
from src.ml_service.preprocessing.French.Vectorize import FrenchVectors
import os
import numpy as np
import seaborn as sns
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

parser = Parser()
j = 0
data = []
sent = []
for i in os.listdir(Global.Precedence_Directory):
    if 'AZ-' in i and j < 1000:
        j += 1
        model = parser.parse(i)
        for topic in model.core_topic:
            vec = FrenchVectors.vectorize_sent(topic)
            data.append(vec)
            sent.append(topic)

data_matrix = np.array(data)
sent = np.array(sent)

hdb = HDBSCAN(min_cluster_size=2).fit(data_matrix)
hdb_labels = hdb.labels_
n_clusters_hdb_ = len(set(hdb_labels)) - (1 if -1 in hdb_labels else 0)

hdb_unique_labels = set(hdb_labels)
hdb_colors = plt.cm.Spectral(np.linspace(0, 1, len(hdb_unique_labels)))
fig = plt.figure(figsize=plt.figaspect(0.5))
hdb_axis = fig.add_subplot('121')
for k, col in zip(hdb_unique_labels, hdb_colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    hdb_axis.plot(data_matrix[hdb_labels == k, 0], data_matrix[hdb_labels == k, 1], 'o', markerfacecolor=col,
                  markeredgecolor='k', markersize=6)

    print(data_matrix[hdb_labels == k, 0])
    print(data_matrix[hdb_labels == k, 1])
    print(sent[hdb_labels == k])
    print('------------------')

hdb_axis.set_title('HDBSCAN\nEstimated number of clusters: %d' % n_clusters_hdb_)
plt.show()