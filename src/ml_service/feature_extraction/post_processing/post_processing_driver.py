from feature_extraction.post_processing.regex import regex_tagger
from feature_extraction.post_processing.regex import regex_lib_helper


def run(command_list):
    """
    Driver for post processing subsystem

    1) Create regex binary
    2) Tag the precedents using the regex
    3) Save vectorized precedents to binary

    :param command_list: Command line arguments
    :return: None
    """
    nb_files = -1
    try:
        nb_files = int(command_list[0])
    except BaseException:
        pass
    regex_lib_helper.create_regex_bin()
    regex_lib_helper.create_regex_cluster_bin(0.5)
    regex_tagger.run(nb_files)
