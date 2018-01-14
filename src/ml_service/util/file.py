import os
import joblib
from enum import Enum
from util.log import Log
from util.constant import Path


class InformationType(Enum):
    SENTENCE = 1
    FILE_NAME = 2
    PROCESSED_SENTENCE = 3


class Save:

    def __init__(self, directory=""):
        """
        Constructor saves models, files
        :param new_directory: String
        """
        self.directory = directory

    def save_binary(self, filename, content):
        """
        Uses joblib implementation over pickle for performance
        and memory. Saves content to binary format
        :param filename: String
        :param content: Object
        :return: None
        """
        file_path = os.path.join(Path.binary_directory, filename)
        Log.write("saving" + filename + " to: " + file_path)
        joblib.dump(content, file_path)
        Log.write(filename + " saved to: " + file_path)

    def save_text(self, data_tuple, labels, protocol="a"):
        """
        Save text file to new directory
        Mainly used for cluster to text
        :param filename: String
        :param text: String or List
        :param protocol: String --> "a", "wb", "w", "a+", "w+"
        :return: None
        """
        unique_labels = set(labels)
        for label in unique_labels:
            text = []
            for i, sent in enumerate(data_tuple[InformationType.SENTENCE.value][labels == label]):
                text.append(sent)
            text.append("\n------------------------------------------\n")

            for i, filename in enumerate(data_tuple[InformationType.FILE_NAME.value][labels == label]):
                text.append(filename)

            target_file_name = str(label) + ".txt"
            file_path = os.path.join(Path.cluster_directory + self.directory + "/", target_file_name)
            Log.write("saving" + target_file_name + " to: " + file_path)
            file = open(file_path, protocol)

            for lines in text:
                # Specific case when writing list of precedent filenames
                file.writelines(lines)
                file.writelines("\n")
            file.close()
            Log.write(target_file_name + " saved to: " + file_path)


class Load:

    @staticmethod
    def load_binary(filename=None):
        """
        Loads binarized facts
        :param: filename: String
        :return: (matrix(sent vectors), list[sentences], list[filenames])
        """
        try:
            Log.write("Loading " + filename)
            file_path = os.path.join(Path.binary_directory, filename)
            file = open(file_path, "rb")
            binary = joblib.load(file)
            Log.write(filename + " is successfully loaded")
            return binary
        except BaseException:
            Log.write(filename + " not found")
