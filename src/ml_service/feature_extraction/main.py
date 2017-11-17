import sys
import time
from ml_models.models import Load
from feature_extraction.clustering.dbscan.dbscan_wrapper import cluster_facts
from feature_extraction.clustering.hdbscan.hdbscan_wrapper import HdbscanTrain
from feature_extraction.clustering.k_means.k_means_wrapper import KMeansWrapper
from feature_extraction.preprocessing import save_model
from outputs.output import Log

'''
Improvement:
1 - Commands can be imporoved for this class. Now a little basic
2 - Perhaps clear previous output directories of the models etc.
'''


def cluster_means(arguments):
    """
    K means clustering
    :param arguments: list[Strings]
    :return: None
    """
    data_tuple = get_precendent_model(arguments[0])
    start = time.time()
    KMeansWrapper(data_tuple)
    done = time.time()
    Log.write('\nClustering time:')
    Log.write(done - start)


def cluster_dbscan(arguments):
    """
    DBSCAN clustering
    :param arguments: list[strings]
    :return: None
    """
    data_tuple = get_precendent_model(arguments[0])
    start = time.time()
    cluster_facts(data_tuple, int(arguments[1]), float(arguments[2]))
    done = time.time()
    Log.write('\nClustering time:')
    Log.write(done - start)


def cluster_hdbscan(arguments):
    """
    HDBSCAN clustering
    :param arguments: list[String]
    :return: None
    """
    data_tuple = get_precendent_model(arguments[0])
    hdb = HdbscanTrain()
    start = time.time()
    hdb.cluster(data_tuple, int(arguments[1]), int(arguments[2]))
    done = time.time()
    Log.write('\nClustering time:')
    Log.write(done - start)


def get_precendent_model(command):
    """
    Selects precedence model based on command
    :param command: string
    :return: None
    """
    if command == '-facts':
        return Load.load_facts_from_bin()
    elif command == '-decisions':
        return Load.load_decisions_from_bin()


def process_command(command, arguments):
    """
    Maps command to function
    :param command: String
    :param arguments: List[string]
    :return: None
    """
    if command == '--dbscan':
        cluster_dbscan(arguments)
    elif command == '--hdbscan':
        cluster_hdbscan(arguments)
    elif command == '--kmeans':
        cluster_means(arguments)
    elif command == '--parse':
        save_model.save()
    else:
        Log.write('Command not recognized:' + command)
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        Log.write('Please provide more arguments')
        sys.exit(1)
    process_command(sys.argv[1], sys.argv[2:])
