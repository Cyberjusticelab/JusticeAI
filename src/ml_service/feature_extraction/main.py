import time
from src.ml_service.feature_extraction.clustering.k_means.k_means_wrapper import KMeansWrapper
from src.ml_service.feature_extraction.clustering.dbscan.dbscan_wrapper import cluster_facts
from src.ml_service.ml_models.models import Load
from src.ml_service.feature_extraction.clustering.hdbscan.hdbscan_wrapper import HdbscanTrain
from src.ml_service.outputs.output import Log
from src.ml_service.feature_extraction.preprocessing.pipe import save_model
import sys

def cluster_means(arguments):
    data_tuple = get_precendece_model(arguments[0])
    start = time.time()
    KMeansWrapper(data_tuple)
    done = time.time()
    Log.write('\nClustering time:')
    Log.write(done - start)


def cluster_dbscan(arguments):
    data_tuple = get_precendece_model(arguments[0])
    start = time.time()
    cluster_facts(data_tuple, int(arguments[1]), int(arguments[2]))
    done = time.time()
    Log.write('\nClustering time:')
    Log.write(done - start)


def cluster_hdbscan(arguments):
    data_tuple = get_precendece_model(arguments[0])
    hdb = HdbscanTrain()
    start = time.time()
    hdb.cluster(data_tuple, int(arguments[1]), int(arguments[2]))
    done = time.time()
    Log.write('\nClustering time:')
    Log.write(done - start)


def get_precendece_model(command):
    if command == '-facts':
        return Load.load_facts_from_bin()
    elif command == '-decisions':
        return Load.load_decisions_from_bin()


def parse_precedence(command):
    data = ''
    if command == '-facts':
        data = 'facts'
    elif command == '-decisions':
        data = 'decisions'
    else:
        Log.write('Command not recognized:' + command)
        sys.exit(1)
    save_model.save(data)

def process_command(command, arguments):
    if command == '--dbscan':
        cluster_dbscan(arguments)
    elif command == '--hdbscan':
        cluster_hdbscan(arguments)
    elif command == '--kmeans':
        cluster_means(arguments)
    elif command == '--parse':
        parse_precedence(arguments[0])
    else:
        Log.write('Command not recognized:' + command)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        Log.write('Please provide more arguments')
        sys.exit(1)

    process_command(sys.argv[1], sys.argv[2:])
