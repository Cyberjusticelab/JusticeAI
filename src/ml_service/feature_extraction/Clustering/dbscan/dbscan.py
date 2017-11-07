# -*- coding: utf-8 -*-
from sklearn.cluster import DBSCAN
import os
import numpy as np
import logging
logger = logging.getLogger('fact_clustering')


def clusterFacts(data_tuple):
    """
        Clusters all given facts using DBSCAN, and writes the resulting
        clusters into different files
        factDict: a Dictionary, where the keys are the sentence strings,
                  and the values are the associated sentence vectors
    """
    X = data_tuple[0]  # sentence vectors
    ms = DBSCAN(min_samples=2, eps=0.4, n_jobs=-1)
    ms.fit(X)
    labels = ms.labels_
    n_clusters = len(np.unique(labels))
    logger.info("Number of estimated clusters : %d" % n_clusters)
    writeFactsToFile(data_tuple, labels)


def writeFactsToFile(data_tuple, labels):
    __script_dir = os.path.abspath(__file__ + "/../")
    __rel_path = r'cluster_dir/'
    outputDirPath = os.path.join(__script_dir, __rel_path)
    if not os.path.exists(outputDirPath):
        os.makedirs(outputDirPath)
    for i in range(len(data_tuple[1])):
        filePath = os.path.join(outputDirPath, str(labels[i]))
        normalizedFilePath = os.path.normpath(filePath)
        f = open(normalizedFilePath + '.txt', 'w')
        f.write('{:.140}'.format(data_tuple[1][i]) + '\n')  # original sentence
        f.writelines(data_tuple[3][i] + '\n')  # processed sentence
        f.writelines(data_tuple[2][i] + '\n\n')  # filename
        f.close()
