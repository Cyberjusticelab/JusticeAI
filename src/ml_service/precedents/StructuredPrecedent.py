from src.ml_service.global_variables.global_variable import InformationType


class StructuredPrecedent:

    FACT_CATEGORY = 0
    FACTS = "facts"
    OUTCOMES = "outcomes"
    LEASE_TERMINATED = "lease_terminated"

    def __init__(self, fact_labels, fact_data_tuple, outcome_labels, outcome_data_tuple):
        """
        :param fact_labels [int]: fact labels/categories for each sentence in the data_tuple
        :param data_tuple <[int], [string], [string]>: vectors, transformed sentences, original sentence
        """
        self.precedents = {}
        self.create_vector(fact_labels, fact_data_tuple, self.FACTS)
        self.create_vector(outcome_labels, outcome_data_tuple, self.OUTCOMES)

    def create_vector(self, labels, data_tuple, data_type):
        """
        Recreates precedents from fact clusters
        :return [[int or None],(int,string)]: Structured precedents where the first element represents the fact vector
                                              The second element contains all the facts, with their category number
        """
        unique_labels = set(labels)
        for label in (temp_label for temp_label in unique_labels if temp_label >= 0):
            for raw_fact_tuple, file_name_tuple in zip(enumerate(data_tuple[InformationType.FACTS.value][labels == label]),
                                                       enumerate(data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][labels == label])):

                file_name = file_name_tuple[1].replace(".txt", "")
                if file_name not in self.precedents:
                    # Create new entry with file name
                    self.precedents[file_name] = dict.fromkeys([self.FACTS, self.OUTCOMES, self.LEASE_TERMINATED])
                    self.precedents[file_name][data_type] = [0] * len(unique_labels)

                self.precedents[file_name][data_type][raw_fact_tuple[self.FACT_CATEGORY]] = 1  # 1 signifies that the fact exists
