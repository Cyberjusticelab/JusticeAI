import numpy
import joblib
import os
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
        self.create_structure_from_data_tuple(fact_labels, fact_data_tuple, self.FACTS)
        self.create_structure_from_data_tuple(decisions_labels, decisions_data_tuple, self.DECISIONS_VECTOR)

    def create_structure_from_data_tuple(self, labels, data_tuple, data_type):
        """
        Creates a fact or decisions vector for all precedents
        :param labels (int): Cluster labels
        :param data_tuple ([int], [string], [string]): vectors, transformed sentences, original sentence
        :param data_type (string): "facts" or "decisions"
        :return: Void
        """
        unique_labels_size = len(set(labels))  # size is reduces by one because we need to ignore "-1" label
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

    def create_structure_from_cluster_files(self, directory, data_type):
        """
        Creates a fact or decisions vector for all precedents
        :param directory (string): directory path where the cluster are located
        :param data_type (string): "facts" or "decisions"
        :return: Void
        """
        vector_size = len([x for x in list(os.scandir(directory)) if x.is_file()]) - 1  # get total file - 1 = vector size

        # loop through each file
        for file in os.listdir(directory):
            label = file.replace(".txt", "")
            if label == "-1":
                continue

            file = open(directory+file, mode='r')
            line = file.readline()

            # Skip each line until the separator is found
            while "----" not in line.strip():
                line = file.readline()

            line = file.readline()  # skip the separator line

            # skip any additional empty line
            while line.strip() == "":
                line = file.readline()

            while line:
                file_name = line.strip().replace(".txt", "")
                if file_name not in self.precedents:
                    # Create new entry with file name
                    self.precedents[file_name] = dict.fromkeys([self.FACTS_VECTOR, self.DECISIONS_VECTOR])

                    # initialize fields
                    self.precedents[file_name][self.FACTS_VECTOR] = numpy.zeros(vector_size, dtype=numpy.int)
                    self.precedents[file_name][self.DECISIONS_VECTOR] = numpy.zeros(vector_size, dtype=numpy.int)

                    # populate fields
                if data_type == self.FACTS:
                    self.precedents[file_name][self.FACTS_VECTOR][int(label)] = 1  # 1 signifies that the fact exists
                else:
                    self.precedents[file_name][self.DECISIONS_VECTOR][int(label)] = 1  # 1 signifies that the fact exists
                line = file.readline()

    def write_data_as_bin(self, dicrectory):
        joblib.dump(self.precedents, dicrectory + "structured_precedent.bin")

if __name__ == '__main__':

    # add paths to fact and decision models
    hdb_facts_model = Load.load_model_from_bin("")
    hdb_decision_model = Load.load_model_from_bin("")
    fact_data_tuple = Load.load_facts_from_bin()
    decision_data_tuple = Load.load_decisions_from_bin()

    precedents = StructuredPrecedent(hdb_facts_model.labels_, fact_data_tuple, hdb_decision_model.labels_, decision_data_tuple)
    precedents.write_data_as_bin(Global.output_directory)


