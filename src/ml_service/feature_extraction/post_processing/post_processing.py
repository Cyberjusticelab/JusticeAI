from feature_extraction.post_processing.precedent_vector.precedent_vector import PrecedentVector
from util.file import Load, Save

def run ():
    fact_cluster_model = Load.load_binary("facts_cluster_model.bin")
    decision_cluster_model = Load.load_binary("decisions_cluster_model.bin")
    fact_data_tuple = Load.load_binary("facts_pre_processed.bin")
    decision_data_tuple = Load.load_binary("decisions_pre_processed.bin")
    precedent_vector = PrecedentVector().create_structure_from_data_tuple(fact_cluster_model.labels_, fact_data_tuple,
                                                      decision_cluster_model.labels_, decision_data_tuple)
    s = Save("precedent_vector")
    s.save_binary("precedent_vector.bin", precedent_vector)
