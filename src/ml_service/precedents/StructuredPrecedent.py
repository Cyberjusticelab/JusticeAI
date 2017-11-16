from global_variables.global_variable import InformationType
from global_variables.global_variable import Global
import json


class StructuredPrecedent:

    CATEGORY_INDEX = 0
    FACTS = "facts"
    FACTS_VECTOR = "facts_vector"
    OUTCOMES = "outcomes"
    OUTCOMES_VECTOR = "outcomes_vector"
    LEASE_TERMINATED = "lease_terminated"

    def __init__(self, fact_labels, fact_data_tuple, outcome_labels, outcome_data_tuple):
        """
        :param fact_labels: Facts cluster labels
        :param fact_data_tuple ([int], [string], [string]): vectors, transformed sentences, original sentence 
        :param outcome_labels: Outcomes cluster labels
        :param outcome_data_tuple ([int], [string], [string]): vectors, transformed sentences, original sentence  
        """
        self.precedents = {}
        self.create_vector(fact_labels, fact_data_tuple, self.FACTS_VECTOR)
        self.create_vector(outcome_labels, outcome_data_tuple, self.OUTCOMES_VECTOR)

    def create_vector(self, labels, data_tuple, data_type):
        """
        Creates a fact or outcome vector for all precedents
        :param labels (int): Cluster labels
        :param data_tuple ([int], [string], [string]): vectors, transformed sentences, original sentence
        :param data_type (string): "facts" or "outcomes"
        :return: Void
        """
        unique_labels = set(labels)
        for label in (temp_label for temp_label in unique_labels if temp_label >= 0):
            for raw_fact_tuple, file_name_tuple in zip(enumerate(data_tuple[InformationType.FACTS.value][labels == label]),
                                                       enumerate(data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][labels == label])):

                file_name = file_name_tuple[1].replace(".txt", "")
                if file_name not in self.precedents:

                    # Create new entry with file name
                    self.precedents[file_name] = dict.fromkeys([self.FACTS, self.FACTS_VECTOR, self.OUTCOMES, self.OUTCOMES_VECTOR, self.LEASE_TERMINATED])

                    # initialize fields
                    if data_type == self.FACTS:
                        self.precedents[file_name][self.FACTS_VECTOR] = [0] * len(unique_labels)
                        self.precedents[file_name][self.FACTS] = []
                    else:
                        self.precedents[file_name][self.OUTCOMES_VECTOR] = [0] * len(unique_labels)
                        self.precedents[file_name][self.OUTCOMES] = []

                # populate fields
                if data_type == self.FACTS:
                    self.precedents[file_name][self.FACTS_VECTOR][raw_fact_tuple[self.CATEGORY_INDEX]] = 1  # 1 signifies that the fact exists
                    self.precedents[file_name][self.FACTS].append(raw_fact_tuple)
                else:
                    self.precedents[file_name][self.OUTCOMES_VECTOR][raw_fact_tuple[self.CATEGORY_INDEX]] = 1  # 1 signifies that the fact exists
                    self.precedents[file_name][self.OUTCOMES].append(raw_fact_tuple)


    def write_data_to_output_dir(self):
        with open(Global.output_directory + "/precedent_JSON.txt", 'w') as outfile:
            json.dump(self.precedents, outfile)
