import regex as re
from feature_extraction.post_processing.regex.regex_lib import RegexLib
from util.file import Save


def get_regexes(name):
    for fact in RegexLib.regex_facts:
        if fact[0] == name:
            return fact[1]
    for demand in RegexLib.regex_demands:
        if demand[0] == name:
            return demand[1]
    for outcome in RegexLib.regex_outcomes:
        if outcome[0] == name:
            return outcome[1]

    # if name was not found in demands, facts or outcomes
    return None


def regex_finder(sentence):
    """
    This function is used to see if a regex is already written for a given sentence
    :param sentence: is used to find a regex the matches it
    :return: list of regex names that matches this sentence
    """
    regex_name_index = 0
    regex_index = 1
    regex_match_list = []

    for fact in RegexLib.regex_facts:
        for reg in fact[regex_index]:
            if re.search(reg, sentence):
                regex_match_list.append(fact[regex_name_index])
    for demand in RegexLib.regex_demands:
        for reg in demand[regex_index]:
            if re.search(reg, sentence):
                regex_match_list.append(demand[regex_name_index])

    return regex_match_list


def sentence_finder(regex_name, nb_of_files):
    """
    finds sentences that matches the regex_name
    :param regex_name: name of the regex ex: landlord_money_cover_rent
    :param nb_of_files: number of files to search through
    :return: list of sentences that matched this regex
    """
    from util.file import Path
    import os
    regexes = get_regexes(regex_name)
    count = 0
    sentences_matched = []
    for i in os.listdir(Path.raw_data_directory):
        if count > nb_of_files:
            break
        count += 1
        file = open(Path.raw_data_directory + i, "r", encoding="ISO-8859-1")
        for line in file:
            for reg in regexes:
                if reg.search(line):
                    sentences_matched.append(line)
        file.close()
    return sentences_matched


def cluster_file_finder(regex_name, min_match_percentage, file_path):
    """
    Given a file path and a regex name, this function validates that at least min_match_percentage (ex: 50%)
    of the sentence matches the regex
    :param regex_name: name of the regex to match with
    :param min_match_percentage: min percentage of matches required
    :param file_path: cluster file path (where the sentences are)
    :return: True if minimum percentage of sentences do matches the given regex
    """
    regexes = get_regexes(regex_name)
    total_nb_lines_in_file = 0
    total_lines_matched = 0
    file = open(file_path, 'r', encoding='ISO-8859-1')
    for line in file:
        if line == '\n':
            break
        total_nb_lines_in_file += 1
        line = '[1] ' + line
        for reg in regexes:
            if reg.search(line):
                total_lines_matched += 1
    file.close()
    if total_lines_matched > 0 and total_lines_matched / total_nb_lines_in_file > min_match_percentage:
        return True
    return False


def cluster_regex_mapper(folder_name, min_match_percentage, nb_of_files=-1):
    """
    This function searches through a given folder_name in order to find all regex-cluster pair and store them in a dict
    :param folder_name: cluster folder to search in (fact or demand)
    :param min_match_percentage: min percentage of sentence in a cluster file that needs to match a regex
    :param nb_of_files: number of files to search through in the folder
    :return: dict of regex-cluster file match
    """
    from util.file import Path
    import os
    nb_of_files_proccessed = 0
    path = Path.cluster_directory + folder_name + '/'
    cluster_regex_dict = {}
    for file_name in os.listdir(path):
        if nb_of_files != -1 and nb_of_files_proccessed > nb_of_files:
            break
        nb_of_files_proccessed += 1
        for regex in RegexLib.regex_facts:
            if cluster_file_finder(regex[0], min_match_percentage, path + file_name):
                if regex[0] in cluster_regex_dict.keys():
                    cluster_regex_dict[regex[0]].append(file_name)
                cluster_regex_dict[regex[0]] = [file_name]
    return cluster_regex_dict


def unpack_fact_demand_bin():
    """
    unpacks fact and demand binaries and move them to their appropriate folders
    :return: None
    """
    from util.file import Path
    import zipfile
    import os
    import shutil
    regex_types = ['fact', 'demand']

    for regex_type in regex_types:
        with zipfile.ZipFile(Path.binary_directory + regex_type + '_cluster.bin', 'r') as zip_ref:
            zip_ref.extractall(Path.cluster_directory)
        for file in os.listdir(Path.cluster_directory + regex_type + '_cluster'):
            shutil.copy(Path.cluster_directory + regex_type + '_cluster/' + file,
                        Path.cluster_directory + regex_type + '/')
        shutil.rmtree(Path.cluster_directory + regex_type + '_cluster/')
        shutil.rmtree(Path.cluster_directory + '__MACOSX/')


def create_regex_cluster_bin(min_match_percentage):
    """

    :param min_match_percentage:
    :return:
    """
    unpack_fact_demand_bin()
    rc_fact_dict = cluster_regex_mapper('fact', min_match_percentage)
    rc_demand_dict = cluster_regex_mapper('demand', min_match_percentage)
    cluster_regex_dict = {'fact': rc_fact_dict, 'demand': rc_demand_dict}
    save = Save()
    save.save_binary('cluster_regex_dict.bin', cluster_regex_dict)


def create_regex_bin():
    """
    Driver to save regex binary file and regex-cluster dict binary
    1) Create an empty dictionary
    2) Add keys and values to the dictionary
    3) binarize file

    :return: None
    """
    regexes = RegexLib()
    reg_dict = {}
    reg_dict['regex_demands'] = regexes.regex_demands
    reg_dict['regex_facts'] = regexes.regex_facts
    reg_dict['regex_outcomes'] = regexes.regex_outcomes
    reg_dict['MONEY_REGEX'] = regexes.MONEY_REGEX
    save = Save()
    save.save_binary('regexes.bin', reg_dict)

create_regex_cluster_bin(0.5)
