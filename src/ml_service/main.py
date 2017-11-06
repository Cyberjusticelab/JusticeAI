# -*- coding: utf-8 -*-
import time
from feature_extraction.Clustering.DBSCAN.fact_clusterer import clusterFacts
from feature_extraction.Preprocessing.fact_extracter import extractFactsFromFiles
from feature_extraction.Preprocessing.related_word_fetcher import save_cache
import logging


def execute():
    logger = logging.getLogger('fact_clustering')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(message)s')
    hdlr = logging.FileHandler('fact_clustering.log')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    start = time.time()
    facts = extractFactsFromFiles(1)
    done = time.time()
    save_cache()

    print('Vectorization time:')
    print(done - start)

    start = time.time()
    clusterFacts(facts)
    done = time.time()

    print('Clustering time:')
    print(done - start)

if __name__ == '__main__':
    execute()
