from feature_extraction.pre_processing import pre_processing
from feature_extraction.clustering import clustering
from feature_extraction.post_processing import post_processing
from util.log import Log

def run(action="all", fact_cluster_method="hdbscan", decision_cluster_method="dbscan", data_type="all"):
    """
    feature_extraction drive
    :param action: String
    :param cluster_type: String
    """
    Log.write("Running feature extraction: (pipleline=" + action + " fact_cluster_algorithm=" + fact_cluster_method +
              " decision_cluster_algorithm=" + decision_cluster_method)
    if action=="pre":
        pre_processing.run()
    elif action=="cluster":
        if data_type=="fact":
            clustering.run(fact_cluster_method, data_type)
        elif data_type=="decision":
            clustering.run(decision_cluster_method, data_type)
        else:
            clustering.run(fact_cluster_method, "fact")
            clustering.run(decision_cluster_method, "decision")
    elif action=="post":
        post_processing.run()
    else:
        pre_processing.run()
        clustering.run(fact_cluster_method, "fact")
        clustering.run(decision_cluster_method, "decision")
        post_processing.run()
