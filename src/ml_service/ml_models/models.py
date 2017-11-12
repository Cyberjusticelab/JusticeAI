import os
import joblib
from src.ml_service.outputs.output import Log

"""
Only store models that are good for use in this directory
"""

class Load():
    __script_dir = os.path.abspath(__file__ + r"/../")
    __processed_facts = 'processed_facts.bin'
    __processed_decisions = 'processed_decisions.bin'

    @staticmethod
    def load_facts_from_bin(filename=None):
        """
        Loads binarized facts
        :param: filename: String
        :return: (matrix, list[strings], list[strings], list[string])
        """
        try:
            Log.write("Loading Preprocessed facts... May take a few seconds")
            file_path = os.path.join(Load.__script_dir, Load.__processed_facts)
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
            file_path = os.path.join(Load.__script_dir, Load.__processed_decisions)
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
