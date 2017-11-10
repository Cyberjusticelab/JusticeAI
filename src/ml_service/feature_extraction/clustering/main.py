import time
from src.ml_service.feature_extraction.clustering.k_means.k_means_wrapper import KMeansWrapper
from src.ml_service.feature_extraction.clustering.dbscan.dbscan import cluster_facts
from src.ml_service.ml_models.models import load_facts_from_bin
import joblib


hdb_supported = False
try:
    from src.ml_service.feature_extraction.clustering.hdbscan_wrapper.Hdbscan import HdbscanTrain
    hdb_supported = True
except:
    pass


def cluster_means(data_tuple):
    start = time.time()
    KMeansWrapper(data_tuple)
    done = time.time()
    print('\nClustering time:')
    print(done - start)


def cluster_dbscan(data_tuple):
    start = time.time()
    model = cluster_facts(data_tuple)
    done = time.time()
    print('\nClustering time:')
    print(done - start)
    return model


def cluster_hdbscan(data_tuple):
    hdb = HdbscanTrain()
    start = time.time()
    model = hdb.train(data_tuple)
    done = time.time()
    print('\nClustering time:')
    print(done - start)
    return model


if __name__ == '__main__':
    precedence = load_facts_from_bin()

    print('DBSCAN begin')
    # comment out what you don't want to cluster
    model = cluster_dbscan(precedence)
    joblib.dump(model, 'dscan_model.bin')

    if hdb_supported:
        print('HDBSCAN begin')
        model = cluster_hdbscan(precedence)
        joblib.dump(model, 'hdb_model.bin')
    else:
        print('HDBSCAN not supported')


