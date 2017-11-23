from feature_extraction import feature_extraction
from model_training import train_model
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
        checkpoint = command_list[1]
        if checkpoint == CommandEnum.PRE_PROCESSING:
            feature_extraction.run(command_list[1:])

        elif checkpoint == CommandEnum.POST_PROCESSING:
            feature_extraction.run(command_list[1:])

        elif checkpoint == CommandEnum.CLUSTERING:
            feature_extraction.run(command_list[1:])

        elif checkpoint == CommandEnum.TRAIN_FACTS:
            train_model.run(command_list[2:])

        else:
            Log.write("Command not recognized: " + command_list[1])


if __name__ == "__main__":
    Command.execute(sys.argv)
