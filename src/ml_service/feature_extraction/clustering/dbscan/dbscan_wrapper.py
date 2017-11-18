from sklearn.cluster import DBSCAN

from util.file import Save
from util.log import Log

class DBSCANWrapper:

    def __init__(self, data_tuple, data_type, min_sample, eps):
        self.data_tuple = data_tuple
        self.min_sample = min_sample
        self.eps = eps
        self.data_type = data_type

    def cluster(self):
        """
        Clusters all given facts using DBSCAN, and writes the resulting
        """
        Log.write("Starting DBSCAN clustering")
        Log.write("Min Epsilon: " + str(self.eps))
        Log.write("Min Sample: " + str(self.min_sample))
        X = self.data_tuple[0]
        db = DBSCAN(min_samples=self.min_sample, eps=self.eps, n_jobs=-1)
        db.fit(X)
        s = Save(self.data_type)
        s.save_binary(self.data_type + "s_cluster_model.bin", db)
        labels = set(db.labels_)
        n_clusters = len(labels) - (1 if -1 in db.labels_ else 0)
        s.save_text(self.data_tuple, labels, "w", 1)
        Log.write("Number of estimated clusters : %d" % n_clusters)
        return db
