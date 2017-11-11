import time
from src.ml_service.feature_extraction.clustering.k_means.k_means_wrapper import KMeansWrapper
from src.ml_service.feature_extraction.clustering.dbscan.dbscan import cluster_facts
from src.ml_service.ml_models.models import load_facts_from_bin
import joblib
from src.ml_service.reporting.logger import Log

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
    data_tuple = None
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
    Log.initialize('log.txt', header='DBSCAN', verbose=True)
    Log.report_start()
    Log.write('Loading precedence')
    precedence = load_facts_from_bin()
    Log.write('Begin DBSCAN')
    # comment out what you don't want to cluster
    model = cluster_dbscan(precedence)
    Log.write('DBSCAN complete')
    Log.write('Saving Model')
    joblib.dump(model, 'dbscan_model.bin')
    Log.report_end()