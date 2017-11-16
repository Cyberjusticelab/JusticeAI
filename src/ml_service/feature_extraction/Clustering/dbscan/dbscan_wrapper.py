# -*- coding: utf-8 -*-
from sklearn.cluster import DBSCAN
import numpy as np
import logging
from global_variables.global_variable import InformationType
from outputs.output import Log, Save


def cluster_facts(data_tuple, min_sample, eps):
    """
    Clusters all given facts using DBSCAN, and writes the resulting
    clusters into different files

    @:param data_tuple <array, array, array>: vectors, transformed sentences, original sentence
    """
    X = data_tuple[0]
    ms = DBSCAN(min_samples=min_sample, eps=eps, n_jobs=-1)
    Log.write('Starting DBSCAN')
    Log.write('Min Epsilon: ' + str(eps))
    Log.write('Min Sample: ' + str(min_sample))
    ms.fit(X)
    s = Save(r'dbscan_model/')
    s.binarize_model('dbscan.bin', ms)
    labels = ms.labels_
    n_clusters = len(np.unique(labels))
    Log.write("Number of estimated clusters : %d" % n_clusters)
    write_facts_to_file(data_tuple, labels)
    return ms


def write_facts_to_file(data_tuple, labels):
    unique_labels = set(labels)
    s = Save('dbscan_cluster_dir')
    for label in unique_labels:
        text = []
        for i, sent in enumerate(data_tuple[InformationType.FACTS.value][labels == label]):
            text.append(sent)
        text.append("\n------------------------------------------\n")

        for i, filename in enumerate(data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][labels == label]):
            text.append(filename)
        s.save_text_file(str(label) + '.txt', text, 'w')
