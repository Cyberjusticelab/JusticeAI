import os
import joblib
from outputs.output import Log

"""
Only store models that are good for use in this directory
"""


class Load():
    script_dir = os.path.abspath(__file__ + "/../")
    __processed_facts = 'processed_facts.bin'
    __processed_decisions = 'processed_decisions.bin'
    fact_cluster_model = 'fact_cluster_model.bin'
    decision_cluster_model = 'decision_cluster_model.bin'
    precedent_vector_from_clusters = 'precedent_vector_from_clusters.bin'
    regex_vectors = 'regex_precedent_dict.bin'

    @staticmethod
    def load_facts_from_bin(filename=None):
        """
        Loads binarized facts
        :param: filename: String
        :return: (matrix(sent vectors), list[sentences], list[filenames])
        """
        try:
            Log.write("Loading Preprocessed facts... May take a few seconds")
            file_path = os.path.join(Load.script_dir, Load.__processed_facts)
            if filename is None:
                file = open(file_path, 'rb')
                model = joblib.load(file)
            else:
                file = open(filename, 'rb')
                model = joblib.load(file)
            Log.write("Loading complete")
            return model
        except BaseException:
            Log.write("Download model binary first")

    @staticmethod
    def load_decisions_from_bin(filename=None):
        """
        Loads binarized facts
        :param: filename: String
        :return: (matrix, list[strings], list[strings], list[[string])
        """
        try:
            Log.write("Loading Preprocessed decisions... May take a few seconds")
            file_path = os.path.join(Load.script_dir, Load.__processed_decisions)
            if filename is None:
                file = open(file_path, 'rb')
                model = joblib.load(file)
            else:
                file = open(filename, 'rb')
                model = joblib.load(file)
            Log.write("Loading complete")
            return model
        except BaseException:
            Log.write("Download model binary first")


    @staticmethod
    def load_model_from_bin(file_name):
        """
        Loads model which matches the file name
        :param: file_path: String
        :return: model
        """
        try:
            Log.write("Loading model... May take a few seconds")
            file_path = os.path.join(Load.script_dir, file_name)
            file = open(file_path, 'rb')
            model = joblib.load(file)
            return model
        except BaseException:
            Log.write("Download the {} model binary first".format(file_name))
