from src.ml_service.feature_extraction.Preprocessing.Sam_Parser.PrecedenceParse import Precedence_Parser
from src.ml_service.GlobalVariables.GlobalVariable import Global
from src.ml_service.feature_extraction.Clustering.k_means.fact_cluster import KMeansWrapper
from src.ml_service.feature_extraction.Clustering.hdbscan_wrapper.Hdbscan import HdbscanTrain
from src.ml_service.feature_extraction.Preprocessing.Arek_Parser import related_word_fetcher
from src.ml_service.feature_extraction.Clustering.dbscan.dbscan import clusterFacts
import time
import numpy


def cluster_means(data_tuple):
    start = time.time()
    wrapper = KMeansWrapper(data_tuple)
    done = time.time()
    print('\nClustering time:')
    print(done - start)


def cluster_dbscan(data_tuple):
    start = time.time()
    clusterFacts(data_tuple)
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
    parser = Precedence_Parser(tfidf=False)
    precedence_dict = parser.parse_files(Global.Precedence_Directory, 10)
    related_word_fetcher.save_cache()

    X = []
    labels = []
    precedence_files = []
    piped_fact = []

    for fact in precedence_dict['facts']:  # replace this variable with 'decisions' for outcomes
        X.append(precedence_dict['facts'][fact].dict['vector'])
        labels += ([precedence_dict['facts'][fact].dict['fact']])
        precedence_files += (precedence_dict['facts'][fact].dict['precedence'])
        piped_fact += ([precedence_dict['facts'][fact].dict['piped_fact']])

    X = numpy.matrix(X)
    labels = numpy.array(labels)
    precedence_files = numpy.array(precedence_files)
    piped_fact = numpy.array(piped_fact)

    data_tuple = (X, labels, precedence_files, piped_fact)

    cluster_dbscan(data_tuple)
    cluster_hdbscan(data_tuple)
    cluster_means(data_tuple)
