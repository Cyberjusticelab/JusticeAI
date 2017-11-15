from src.ml_service.GlobalVariables.GlobalVariable import InformationType


class StructuredPrecedent:

    FACT_LABEL = 0
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
        for label in set(self.fact_labels):
            for raw_fact_tuple, file_name_tuple in zip(enumerate(self.data_tuple[InformationType.FACTS.value][self.fact_labels == label]),
                                                       enumerate(self.data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][self.fact_labels == label])):

                file_name = file_name_tuple[1].replace(".txt", "")
                if file_name not in precedents:
                    precedents[file_name] = [[None]*len(self.fact_labels), [raw_fact_tuple]]
                else:
                    precedents[file_name][self.FACT_TUPLE].append(raw_fact_tuple)

                precedents[file_name][self.FACT_VECTOR][raw_fact_tuple[self.FACT_LABEL]] = 1
        return precedents
