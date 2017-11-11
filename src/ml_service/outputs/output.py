import joblib
import os
import logging
import os

class Log:
    __output_dir = os.path.abspath(__file__ + r"/../")
    __rel_path = 'server.log'
    __filename = os.path.join(__output_dir, __rel_path)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s: %(message)s',
                        datefmt='%y/%m/%d-%H:%M:%S',
                        filename=__filename,
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-0s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__filename)

    @staticmethod
    def write(text):
        Log.logger.info(text)

class Save():

    def __init__(self, directory=''):
        """
        Constructor creates a new directory to save models, files in
        :param new_directory: String
        """
        self.__output_dir = os.path.abspath(__file__ + r"/../")
        if directory != '':
            __rel_path = directory
            dir_path = os.path.join(self.__output_dir, __rel_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            self.__output_dir = os.path.abspath(__file__ + r"/../" + directory + '/')



    def binarize_model(self, filename, model):
        """
        Uses joblib implementation over pickle for performance
        and memory. Saves model to binary format
        :param filename: String
        :param model: Object
        :return: None
        """
        __rel_path = filename
        file_path = os.path.join(self.__output_dir, __rel_path)
        joblib.dump(model, file_path)
        Log.write('Model saved to: ' + file_path)


    def save_text_file(self, filename, text,protocol='a'):
        """
        Save text file to new directory
        :param filename: String
        :param text: String or List
        :param protocol: String --> 'a', 'wb', 'w', 'a+', 'w+'
        :return: None
        """
        __rel_path = filename
        file_path = os.path.join(self.__output_dir, __rel_path)
        file = open(file_path, protocol)
        if not type(text) == list:
            text = [text]
        for lines in text:
            file.writelines(lines)
            file.writelines('\n')
        file.close()