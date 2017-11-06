# -*- coding: utf-8 -*-
import time
import dbscan.fact_clusterer
import fact_extracter
import related_word_fetcher
import logging

logger = logging.getLogger('fact_clustering')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(module)s - %(message)s')
hdlr = logging.FileHandler('fact_clustering.log')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)


start = time.time()
facts = fact_extracter.extractFactsFromFiles(1)
done = time.time()
related_word_fetcher.save_cache()
print('Vectorization time:')
print(done - start)

start = time.time()
dbscan.fact_clusterer.clusterFacts(facts)
done = time.time()

print('Clustering time:')
print(done - start)
