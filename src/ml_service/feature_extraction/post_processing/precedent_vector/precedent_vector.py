import os
import joblib
import numpy

from util.file import Load, InformationType
from util.constant import Path

class PrecedentVector:

    FACTS = "facts"
    FACTS_VECTOR = "facts_vector"
    DECISIONS = "decisions"
    DECISIONS_VECTOR = "decisions_vector"

    def __init__(self):
        self.precedents = {}

    def create_structure_from_cluster_files(self, fact_cluster_directory, decision_cluster_directory):
        """
        :param fact_cluster_directory (string): directory path to fact clusters
        :param decision_cluster_directory (string): directory path to decision clusters
        :return: 
        """
        self.__create_structure_from_cluster_files(fact_cluster_directory, self.FACTS)
        self.__create_structure_from_cluster_files(decision_cluster_directory ,self.DECISIONS)

    def create_structure_from_data_tuple(self, fact_labels, fact_data_tuple, decisions_labels, decisions_data_tuple):
        """
        :param fact_labels: Facts cluster labels
        :param fact_data_tuple ([int], [string], [string]): vectors, transformed sentences, original sentence
        :param decisions_labels: Decisions cluster labels
        :param Decisions_data_tuple ([int], [string], [string]): vectors, transformed sentences, original sentence
        """

        self.__create_structure_from_data_tuple(fact_labels, fact_data_tuple, self.FACTS)
        self.__create_structure_from_data_tuple(decisions_labels, decisions_data_tuple, self.DECISIONS)

    def __create_structure_from_data_tuple(self, labels, data_tuple, data_type):
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

            for file_name in data_tuple[InformationType.FILE_NAME.value][index]:
                file_name = file_name.strip().replace(".txt", "")
                if file_name not in self.precedents:

                    # Create new entry with file name
                    self.precedents[file_name] = dict.fromkeys([self.FACTS_VECTOR, self.DECISIONS_VECTOR])

                if data_type == self.FACTS:

                    # initialize fields
                    if self.precedents[file_name][self.FACTS_VECTOR] is None:
                        self.precedents[file_name][self.FACTS_VECTOR] = numpy.zeros(unique_labels_size, dtype=numpy.int)

                    # populate fields
                    self.precedents[file_name][self.FACTS_VECTOR][label] = 1  # 1 signifies that the fact exists
                else:

                    # initialize fields
                    if self.precedents[file_name][self.DECISIONS_VECTOR] is None:
                        self.precedents[file_name][self.DECISIONS_VECTOR] = numpy.zeros(unique_labels_size, dtype=numpy.int)

                    # populate fields
                    self.precedents[file_name][self.DECISIONS_VECTOR][label] = 1  # 1 signifies that the fact exists

    def __create_structure_from_cluster_files(self, directory, data_type):
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
                if data_type == self.FACTS:

                    # initialize fields
                    if self.precedents[file_name][self.FACTS_VECTOR] is None:
                        self.precedents[file_name][self.FACTS_VECTOR] = numpy.zeros(vector_size, dtype=numpy.int)

                    # populate fields
                    self.precedents[file_name][self.FACTS_VECTOR][int(label)] = 1  # 1 signifies that the fact exists
                else:

                    # initialize fields
                    if self.precedents[file_name][self.DECISIONS_VECTOR] is None:
                        self.precedents[file_name][self.DECISIONS_VECTOR] = numpy.zeros(vector_size, dtype=numpy.int)

                    # populate fields
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

    structured_precedent = PrecedentVector()
    structured_precedent.create_structure_from_data_tuple(hdb_facts_model.labels_, fact_data_tuple, hdb_decision_model.labels_, decision_data_tuple)

    structured_precedent.write_data_as_bin(Path.output_directory)
