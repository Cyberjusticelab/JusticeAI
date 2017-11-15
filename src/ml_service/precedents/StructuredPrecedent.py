from src.ml_service.global_variables.global_variable import InformationType


class StructuredPrecedent:

    FACT_CATEGORY = 0
    FACT_VECTOR = 0
    FACT_TUPLE = 1

    def __init__(self, fact_labels, data_tuple):
        """
        :param fact_labels [int]: fact labels/categories for each sentence in the data_tuple
        :param data_tuple <[int], [string], [string]>: vectors, transformed sentences, original sentence
        """
        self.fact_labels = fact_labels
        self.data_tuple = data_tuple

    def get_precedents(self):
        """
        Recreates precedents from fact clusters
        :return [[int or None],(int,string)]: Structured precedents where the first element represents the fact vector
                                              The second element contains all the facts, with their category number
        """
        precedents = {}
        unique_labels = set(self.fact_labels)
        for label in unique_labels:
            for raw_fact_tuple, file_name_tuple in zip(enumerate(self.data_tuple[InformationType.FACTS.value][self.fact_labels == label]),
                                                       enumerate(self.data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][self.fact_labels == label])):

                file_name = file_name_tuple[1].replace(".txt", "")
                if file_name not in precedents:
                    # Create new entry with file name
                    precedents[file_name] = [[None]*len(unique_labels), [raw_fact_tuple]]
                else:
                    # add fact to existing entry
                    precedents[file_name][self.FACT_TUPLE].append(raw_fact_tuple)

                precedents[file_name][self.FACT_VECTOR][raw_fact_tuple[self.FACT_CATEGORY]] = 1  # 1 signifies that the fact exists
        return precedents
