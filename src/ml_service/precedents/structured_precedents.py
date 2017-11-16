import numpy
import joblib
from global_variables.global_variable import InformationType
from global_variables.global_variable import Global
from ml_models.models import Load


class StructuredPrecedent:

    FACTS = "facts"
    FACTS_VECTOR = "facts_vector"
    DECISIONS = "decisions"
    DECISIONS_VECTOR = "decisions_vector"

    def __init__(self, fact_labels, fact_data_tuple, decisions_labels, decisions_data_tuple):
        """
        :param fact_labels: Facts cluster labels
        :param fact_data_tuple ([int], [string], [string]): vectors, transformed sentences, original sentence 
        :param decisions_labels: Decisions cluster labels
        :param Decisions_data_tuple ([int], [string], [string]): vectors, transformed sentences, original sentence  
        """
        self.precedents = {}
        self.create_vector(fact_labels, fact_data_tuple, self.FACTS)
        self.create_vector(decisions_labels, decisions_data_tuple, self.DECISIONS_VECTOR)
        self.write_data_as_bin()

    def create_vector(self, labels, data_tuple, data_type):
        """
        Creates a fact or decisions vector for all precedents
        :param labels (int): Cluster labels
        :param data_tuple ([int], [string], [string]): vectors, transformed sentences, original sentence
        :param data_type (string): "facts" or "decisions"
        :return: Void
        """
        unique_labels_size = len(set(labels)) - 1  # size is reduces by one because we need to ignore label -1
        for index, label in enumerate(labels):
            if label < 0:
                continue

            raw_fact = data_tuple[InformationType.FACTS.value][index]

            for file_name in data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][index]:
                file_name = file_name.replace(".txt", "")
                if file_name not in self.precedents:

                    # Create new entry with file name
                    self.precedents[file_name] = dict.fromkeys([self.FACTS, self.FACTS_VECTOR, self.DECISIONS, self.DECISIONS_VECTOR])

                    # initialize fields
                    self.precedents[file_name][self.FACTS_VECTOR] = numpy.zeros(unique_labels_size, dtype=numpy.int)
                    self.precedents[file_name][self.FACTS] = []
                    self.precedents[file_name][self.DECISIONS_VECTOR] = numpy.zeros(unique_labels_size, dtype=numpy.int)
                    self.precedents[file_name][self.DECISIONS] = []

                # populate fields
                if data_type == self.FACTS:
                    self.precedents[file_name][self.FACTS_VECTOR][label] = 1  # 1 signifies that the fact exists
                    self.precedents[file_name][self.FACTS].append(raw_fact)
                else:
                    self.precedents[file_name][self.DECISIONS_VECTOR][label] = 1  # 1 signifies that the fact exists
                    self.precedents[file_name][self.DECISIONS].append(raw_fact)

    def write_data_as_bin(self, dicrectory):
        joblib.dump(self.precedents, dicrectory + "structured_precedent.bin")

if __name__ == '__main__':

    # add paths for fact and decision models
    hdb_facts_model = Load.load_model_from_bin("")
    hdb_decision_model = Load.load_model_from_bin("")
    fact_data_tuple = Load.load_facts_from_bin()
    decision_data_tuple = Load.load_decisions_from_bin()

    precedents = StructuredPrecedent(hdb_facts_model, fact_data_tuple, hdb_decision_model, decision_data_tuple)
    precedents.write_data_as_bin(Global.output_directory)

