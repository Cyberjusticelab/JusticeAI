from feature_extraction.pre_processing import pre_processing
from feature_extraction.clustering import clustering
from util.log import Log

def feature_extraction(action="all", cluster_method="hdbscan", data_type="all"):
    """
    feature_extraction drive
    :param action: String
    :param cluster_type: String
    """
    Log.write("Running feature extraction: (pipleline=" + action + " cluter_algorithm=" + cluster_method + " data_type=" + data_type)
    if action=="pre":
        pre_processing.pre_processing()
    elif action=="cluster":
        if data_type=="all":
            clustering.clustering(cluster_method, "fact")
            clustering.clustering(cluster_method, "decision")
        else:
            clustering.clustering(cluster_method, data_type)
    elif action=="post":
        pass
    else:
        pre_processing.pre_processing()
        clustering.clustering(cluster_method, data_type)

feature_extraction("cluster", "dbscan", "decision")