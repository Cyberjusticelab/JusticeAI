# -*- coding: utf-8 -*-
import time
from src.ml_service.feature_extraction.Clustering.dbscan import dbscan
from src.ml_service.feature_extraction.Preprocessing.Arek_Parser import fact_extracter
from src.ml_service.feature_extraction.Preprocessing.Arek_Parser import related_word_fetcher
import logging

if __name__ == '__main__':
    logger = logging.getLogger('fact_clustering')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(message)s')
    hdlr = logging.FileHandler('fact_clustering.log')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    start = time.time()
    facts = fact_extracter.extractFactsFromFiles(30)
    done = time.time()
    related_word_fetcher.save_cache()
    print('Vectorization time:')
    print(done - start)

    start = time.time()
    dbscan.clusterFacts(facts)
    done = time.time()

    print('Clustering time:')
    print(done - start)
