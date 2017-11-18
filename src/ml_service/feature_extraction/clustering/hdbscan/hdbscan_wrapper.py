from hdbscan import HDBSCAN

from feature_extraction.clustering.constant import InformationType
from util.file import Save
from util.log import Log


def cluster(data_tuple, min_cluster_size, min_sample, type):
    """
    Clusters all given facts using HDBSCAN, and writes the resulting
    clusters into different files

    @:param data_tuple (matrix<vectors>, List<String: sentences>, List<String: filenames>)
    """
    Log.write("Starting HDBSCAN clustering")
    Log.write("Min Cluster Size: " + str(min_cluster_size))
    Log.write("Min Sample: " + str(min_sample))
    X = data_tuple[0]
    hdb = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_sample)
    hdb.fit(X)
    s = Save(r"hdbscan_clusters")
    s.save_binary("hdbscan_" + type + ".bin", hdb)
    labels = set(hdb.labels_)
    n_clusters = len(labels) - (1 if -1 in hdb.labels_ else 0)
    write_cluster_to_file(data_tuple, labels)
    Log.write("Number of estimated clusters : %d" % n_clusters)
    return hdb

def write_cluster_to_file(data_tuple, labels):
    """
    Writes 1 text file per cluster
    The sentences from the files are enumerated in the file
    followed by the cases in which they appear (filenames)

    @:param unique_labels <int>: index of vector
    @:param labels <int>: index of vector
    @:param data_tuple <matrix, array, array>:
            Sentence vectors, String sentences, String filenames
    """
    s = Save(r"hdbscan_clusters")
    for label in labels:
        text = []
        for i, sent in enumerate(data_tuple[InformationType.FACTS.value][labels == label]):
            text.append(sent)
        text.append("\n------------------------------------------\n")

        for i, filename in enumerate(data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][labels == label]):
            text.append(filename)
        s.save_text(str(label) + ".txt", text, "w")


