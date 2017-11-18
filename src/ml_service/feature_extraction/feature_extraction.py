from feature_extraction.pre_processing import pre_processing
from feature_extraction.clustering import clustering
from util.log import Log

def feature_extraction(action="all", cluster_method="hdbscan", data_type="fact"):
    """
    feature_extraction drive
    :param action: String
    :param cluster_type: String
    """
    Log.write("Running feature extraction\naction=" + action)
    if action=="pre":
        pre_processing.save()
    elif action=="cluster":
        clustering.clustering(cluster_method, data_type)
    elif action=="post":
        pass
    else:
        pre_processing.save()
        clustering.clustering(cluster_method, data_type)