import time
import fact_clusterer
import fact_extracter

start = time.time()
facts = fact_extracter.extractFactsFromFiles(100)
done = time.time()

print('Vectorization time:')
print(done - start)

start = time.time()
fact_clusterer.clusterFacts(facts)
done = time.time()

print('Clustering time:')
print(done - start)
