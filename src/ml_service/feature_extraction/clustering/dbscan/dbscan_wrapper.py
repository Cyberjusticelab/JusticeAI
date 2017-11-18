import numpy as np
from sklearn.cluster import DBSCAN

from feature_extraction.clustering.constant import InformationType
from util.file import Save
from util.log import Log


def cluster_facts(data_tuple, min_sample, eps, type):
    """
    Clusters all given facts using DBSCAN, and writes the resulting
    clusters into different files

    @:param data_tuple <array, array, array>: vectors, transformed sentences, original sentence
    """
    Log.write("Starting DBSCAN clustering")
    Log.write("Min Epsilon: " + str(eps))
    Log.write("Min Sample: " + str(min_sample))
    X = data_tuple[0]
    db = DBSCAN(min_samples=min_sample, eps=eps, n_jobs=-1)
    db.fit(X)
    s = Save(r"dbscan_clusters")
    s.save_binary("dbscan_" + type + ".bin", db)
    labels = set(db.labels_)
    n_clusters = len(labels) - (1 if -1 in db.labels_ else 0)
    write_cluster_to_file(data_tuple, labels)
    Log.write("Number of estimated clusters : %d" % n_clusters)
    return db


def write_cluster_to_file(data_tuple, labels):
    """
    Writes 1 text file per cluster
    The sentences from the files are enumerated in the file
    followed by the cases in which they appear (filenames)

    @:param unique_labels <int>: index of vector
    @:param labels <int>: index of vector
    @:param data_tuple <matrix, array, array>:
            Sentence vectors, String sentences, String filenames
    """
    s = Save(r"dbscan_clusters")
    for label in labels:
        text = []
        for i, sent in enumerate(data_tuple[InformationType.FACTS.value][labels == label]):
            text.append(sent)
        text.append("\n------------------------------------------\n")

        for i, filename in enumerate(data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][labels == label]):
            text.append(filename)
        s.save_text(str(label) + ".txt", text, "w")
