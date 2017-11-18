from sklearn.cluster import KMeans

from util.file import Save
from util.log import Log

class KMeansWrapper:

    def __init__(self, data_tuple, data_type, cluster_size=100, method="k-means++"):
        self.data_tuple = data_tuple
        self.data_type = data_type
        self.cluster_size = cluster_size
        self.method = method

    def cluster(self):
        """
        Clusters all given facts using K-Mean, and writes the resulting
        """
        Log.write("Starting K-Mean clustering")
        Log.write("Cluster Size: " + str(self.cluster_size))
        Log.write("K-Mean Method: " + str(self.method))
        X = self.data_tuple[0]
        km = KMeans(n_clusters=self.cluster_size, init=self.method)
        km.fit(X)
        s = Save(self.data_type)
        s.save_binary(self.data_type + "s_cluster_model.bin", km)
        labels = set(km.labels_)
        s.save_text(self.data_tuple, labels, "w", 1)
        Log.write("Number of estimated clusters : %d" % self.cluster_size)
        return km