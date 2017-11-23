import time

from feature_extraction.clustering.dbscan.dbscan_wrapper import DBSCANWrapper
from feature_extraction.clustering.hdbscan.hdbscan_wrapper import HDBSCANWrapper
from feature_extraction.clustering.k_means.k_means_wrapper import KMeansWrapper
from util.file import Load
from util.log import Log


class CommandEnum:
    DBSCAN = '--dbscan'
    HDBSCAN = '--hdbscan'
    KMEANS = '--kmeans'
    FACTS = '--fact'
    OUTCOMES = '--decision'


def dbscan(data_tuple, data_type, command_list):
    try:
        min_cluster_size = int(command_list[0])
        epsilon = float(command_list[1])
        DBSCANWrapper(data_tuple, data_type, min_cluster_size, epsilon).cluster()
        return True
    except ValueError:
        Log.write("Commands must be numerics")
        return False


def hdbscan(data_tuple, data_type, command_list):
    try:
        min_cluster_size = int(command_list[0])
        min_sample_size = int(command_list[1])
        HDBSCANWrapper(data_tuple, data_type, min_cluster_size, min_sample_size).cluster()
        return True
    except ValueError:
        Log.write("Commands must be numerics")
        return False


def kmeans(data_tuple, data_type, command_list):
    try:
        cluster_size = int(command_list[0])
        KMeansWrapper(data_tuple, data_type, cluster_size=cluster_size).cluster()
        return True
    except ValueError:
        Log.write("Commands must be numerics")
        return False


def get_data_tuple(data_type):
    if data_type == CommandEnum.FACTS:
        return Load.load_binary("facts_pre_processed.bin")
    elif data_type == CommandEnum.OUTCOMES:
        return Load.load_binary("decisions_pre_processed.bin")
    else:
        Log.write("Command not recognized: " + data_type)


def run(command_list):
    if len(command_list) < 2:
        return False

    method = command_list[0]
    data_type = command_list[1]

    start = time.time()
    data_tuple = get_data_tuple(data_type)

    if data_tuple is None:
        return False

    data_type = data_type.replace("--", "")

    success = False

    if method == CommandEnum.HDBSCAN:
        success = hdbscan(data_tuple, data_type, command_list[2:])

    elif method == CommandEnum.DBSCAN:
        success = dbscan(data_tuple, data_type, command_list[2:])

    elif method == CommandEnum.KMEANS:
        success = kmeans(data_tuple, data_type, command_list[2:])

    else:
        Log.write("Command not recognized: " + method)

    done = time.time()
    Log.write("Clustering time: " + str(done - start))
    return success
