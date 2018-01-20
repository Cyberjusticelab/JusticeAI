from feature_extraction import feature_extraction_driver
from model_training import training_driver
from util.log import Log
import sys


class CommandEnum:
    PRE_PROCESSING = "-pre"
    POST_PROCESSING = "-post"
    CLUSTERING = "-cluster"
    TRAIN_FACTS = '-train'


class Command:
    @staticmethod
    def execute(command_list):
        """
        Executes machine learning with command line
        Example Usage: 
        1) python3 main.py -cluster --hdbscan --fact 1 2
        2) python3 main.py -pre 10000
        3) python3 main.py -post
        4) python3 main.py -train
        :param command_list: Command line arguments
        :return: None
        """
        checkpoint = command_list[1]
        if checkpoint == CommandEnum.PRE_PROCESSING:
            feature_extraction_driver.run(command_list[1:])

        elif checkpoint == CommandEnum.POST_PROCESSING:
            feature_extraction_driver.run(command_list[1:])

        elif checkpoint == CommandEnum.CLUSTERING:
            feature_extraction_driver.run(command_list[1:])

        elif checkpoint == CommandEnum.TRAIN_FACTS:
            training_driver.run(command_list[2:])

        else:
            Log.write("Command not recognized: " + command_list[1])
            return False
        return True


if __name__ == "__main__":
    Command.execute(sys.argv)
