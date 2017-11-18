import time

from feature_extraction.clustering.dbscan.dbscan_wrapper import DBSCANWrapper
from feature_extraction.clustering.hdbscan.hdbscan_wrapper import HDBSCANWrapper
from feature_extraction.clustering.k_means.k_means_wrapper import KMeansWrapper
from util.file import Load
from util.log import Log

def clustering(cluster_method, data_type):
    start = time.time()
    data_tuple = get_precendent_model(data_type)
    if cluster_method == "dbscan":
        DBSCANWrapper(data_tuple, data_type, 10, 0.3).cluster()
    elif cluster_method == "k-mean":
        KMeansWrapper(data_tuple, data_type).cluster()
    else:
        HDBSCANWrapper(data_tuple, data_type, 20, 5).cluster()
    done = time.time()
    Log.write("Clustering time: " + (done - start))

def get_precendent_model(data_type):
    """
    Selects precedence model based on command
    :param command: string
    :return: None
    """
    if data_type == "fact":
        return Load.load_binary("pre_processed_facts.bin")
    elif data_type == "decision":
        return Load.load_binary("pre_processed_decisions")