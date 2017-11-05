# -*- coding: utf-8 -*-
from sklearn.cluster import DBSCAN
import os
import numpy as np
import time
import logging
logger = logging.getLogger('fact_clustering')


def clusterFacts(factDict):
    """
        Clusters all given facts using DBSCAN, and writes the resulting
        clusters into different files
        factDict: a Dictionary, where the keys are the sentence strings,
                  and the values are the associated sentence vectors
    """
    X = np.matrix(list(factDict.values()))
    ms = DBSCAN()
    ms.fit(X)
    labels = ms.labels_
    n_clusters = len(np.unique(labels))
    logger.info("Number of estimated clusters : %d" % n_clusters)
    writeFactsToFile(factDict, labels)


def writeFactsToFile(factDict, labels):
    outputDirPath = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), '../../../outputs/')
    for i, sent in enumerate(factDict.keys()):
        filePath = os.path.join(outputDirPath, str(labels[i]))
        normalizedFilePath = os.path.normpath(filePath)
        f = open(normalizedFilePath, 'a', encoding="ISO-8859-1")
        f.write('{:.140}'.format(sent) + '\n')
        f.close()
