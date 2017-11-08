import time
import numpy
from src.ml_service.feature_extraction.Preprocessing.Sam_Parser.PrecedenceParse import Precedence_Parser
from src.ml_service.GlobalVariables.GlobalVariable import Global
from src.ml_service.feature_extraction.Clustering.k_means.k_means_wrapper import KMeansWrapper
from src.ml_service.feature_extraction.Preprocessing.Arek_Parser import related_word_fetcher
from src.ml_service.feature_extraction.Clustering.dbscan.dbscan import cluster_facts
hdb_supported = False
try:
    from src.ml_service.feature_extraction.Clustering.hdbscan_wrapper.Hdbscan import HdbscanTrain
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
    cluster_facts(data_tuple)
    done = time.time()
    print('\nClustering time:')
    print(done - start)


def cluster_hdbscan(data_tuple):
    hdb = HdbscanTrain()
    start = time.time()
    hdb.train(data_tuple)
    done = time.time()
    print('\nClustering time:')
    print(done - start)


if __name__ == '__main__':
    # set tf-idf to true if you want to use it
    tf = False
    nb_files = 100
    data_to_extract = 'facts'  # replace this variable with 'facts' for facts and 'decisions' for outcomes

    parser = Precedence_Parser(tfidf=tf)
    print('TF-IDF set to: ' + str(tf))
    print('Reading: ' + str(nb_files) + " files")
    precedence_dict = parser.parse_files(Global.Precedence_Directory, nb_files)
    print()
    print('Preprocessing complete')
    related_word_fetcher.save_cache()
    print('Word cache saved')

    X = []
    labels = []
    precedence_files = []
    piped_fact = []
    print('Loading information from dictionary into format for clustering')
    for fact in precedence_dict[data_to_extract]:
        X.append(precedence_dict[data_to_extract][fact].dict['vector'])
        labels += ([precedence_dict[data_to_extract][fact].dict['fact']])
        precedence_files += (precedence_dict[data_to_extract][fact].dict['precedence'])
        piped_fact += ([precedence_dict[data_to_extract][fact].dict['piped_fact']])

    print('Transforming informaiton into matrix')
    X = numpy.matrix(X)
    labels = numpy.array(labels)
    precedence_files = numpy.array(precedence_files)
    piped_fact = numpy.array(piped_fact)

    data_tuple = (X, labels, precedence_files, piped_fact)

    print('DBSCAN begin')
    # comment out what you don't want to cluster
    cluster_dbscan(data_tuple)

    if hdb_supported:
        print('HDBSCAN begin')
        cluster_hdbscan(data_tuple)
    else:
        print('HDBSCAN not supported')
    print('K-MEANS begin')
    cluster_means(data_tuple)
