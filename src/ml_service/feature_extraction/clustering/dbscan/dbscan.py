# -*- coding: utf-8 -*-
from sklearn.cluster import DBSCAN
import os
import numpy as np
import logging
from src.ml_service.global_variables.global_variable import InformationType
logger = logging.getLogger('fact_clustering')
from src.ml_service.reporting.logger import Log

def cluster_facts(data_tuple):
    """
    Clusters all given facts using DBSCAN, and writes the resulting
    clusters into different files

    @:param data_tuple <array, array, array>: vectors, transformed sentences, original sentence
    """
    X = data_tuple[0]
    data_tuple = None
    ms = DBSCAN(min_samples=5, eps=1, n_jobs=-1)
    ms.fit(X)
    labels = ms.labels_
    n_clusters = len(np.unique(labels))
    Log.write("Number of estimated clusters : %d" % n_clusters)
    #write_facts_to_file(data_tuple, labels)
    return ms


def write_facts_to_file(data_tuple, labels):
    __script_dir = os.path.abspath(__file__ + "/../")
    __rel_path = r'cluster_dir/'
    output_directory = os.path.join(__script_dir, __rel_path)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    unique_labels = set(labels)
    for label in unique_labels:
        file = open(output_directory + str(label) + '.txt', 'w')

        for i, sent in enumerate(data_tuple[InformationType.FACTS.value][labels == label]):
            file.writelines(sent + '\n')  # original sentence

        file.writelines("-------------------------\n")
        for i, process_sent in enumerate(data_tuple[InformationType.PROCESSED_FACTS.value][labels == label]):
            file.writelines(process_sent + '\n')  # processed sentence

        file.writelines("-------------------------\n")
        for i, filename in enumerate(data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][labels == label]):
            file.writelines(filename + '\n')  # filename

        file.close()
