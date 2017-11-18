from hdbscan import HDBSCAN

from util.file import Save
from util.log import Log

class HDBSCANWrapper:

    def __init__(self, data_tuple, min_cluster_size, min_sample, type):
        self.data_tuple = data_tuple
        self.min_cluster_size = min_cluster_size
        self.min_sample = min_sample
        self.type = type

    def cluster(self):
        """
        Clusters all given facts using HDBSCAN, and writes the resulting
        """
        Log.write("Starting HDBSCAN clustering")
        Log.write("Min Cluster Size: " + str(self.min_cluster_size))
        Log.write("Min Sample: " + str(self.min_sample))
        X = self.data_tuple[0]
        hdb = HDBSCAN(min_cluster_size=self.min_cluster_size, min_samples=self.min_sample)
        hdb.fit(X)
        s = Save(r"hdbscan_clusters")
        s.save_binary(self.type + ".bin", hdb)
        labels = set(hdb.labels_)
        n_clusters = len(labels) - (1 if -1 in hdb.labels_ else 0)
        s.save_text(self.data_tuple, labels, "w")
        Log.write("Number of estimated clusters : %d" % n_clusters)
        return hdb