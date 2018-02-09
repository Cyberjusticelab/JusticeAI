from feature_extraction.pre_processing import pre_processing_driver
from feature_extraction.post_processing import post_processing_driver
from util.log import Log


class CommandEnum:
    PRE_PROCESSING = "-pre"
    POST_PROCESSING = "-post"


def run(command_list):
    """
    Driver for feature extraction subsystem
    :param command_list: Command line arguments
    :return: None
    """
    command = command_list[0]
    if command == CommandEnum.PRE_PROCESSING:
        pre_processing_driver.run(command_list[1:])

    elif command == CommandEnum.POST_PROCESSING:
        post_processing_driver.run(command_list[1:])
    else:
        Log.write("Command not recognized: " + command_list[0])
        return False
    return True
