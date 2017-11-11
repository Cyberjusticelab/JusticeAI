import time
from src.ml_service.feature_extraction.clustering.k_means.k_means_wrapper import KMeansWrapper
from src.ml_service.feature_extraction.clustering.dbscan.dbscan_wrapper import cluster_facts
from src.ml_service.ml_models.models import Load
import joblib
from src.ml_service.feature_extraction.clustering.hdbscan.hdbscan_wrapper import HdbscanTrain
import sys

def cluster_means(data_tuple):
    start = time.time()
    KMeansWrapper(data_tuple)
    done = time.time()
    print('\nClustering time:')
    print(done - start)


def cluster_dbscan(data_tuple):
    start = time.time()
    model = cluster_facts(data_tuple)
    data_tuple = None
    done = time.time()
    print('\nClustering time:')
    print(done - start)
    return model


def cluster_hdbscan(data_tuple):
    hdb = HdbscanTrain()
    start = time.time()
    model = hdb.cluster(data_tuple)
    done = time.time()
    print('\nClustering time:')
    print(done - start)
    return model


if __name__ == '__main__':
    precedence = Load.load_decisions_from_bin()
    # comment out what you don't want to cluster
    print('start')
    model = cluster_hdbscan(precedence)
    print('end')
    joblib.dump(model, 'hdbscan_model.bin')