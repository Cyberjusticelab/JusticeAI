"""

"""
import regex as re
import os
from feature_extraction.post_processing.regex.regex_lib import RegexLib
from util.file import Path

regex_name_index = 0
regex_index = 1


def get_regexes(name):
    for fact in RegexLib.regex_facts:
        if fact[regex_name_index] == name:
            return fact[regex_index]
    for demand in RegexLib.regex_demands:
        if demand[regex_name_index] == name:
            return demand[regex_index]
    for outcome in RegexLib.regex_outcomes:
        if outcome[regex_name_index] == name:
            return outcome[regex_index]

    # if name was not found in demands, facts or outcomes
    return None


def regex_finder(sentence):
    """
    This function is used to see if a regex is already written for a given sentence
    :param sentence: is used to find a regex the matches it
    :return: list of regex names that matches this sentence
    """
    regex_match_list = []

    for fact in RegexLib.regex_facts:
        for reg in fact[regex_index]:
            if re.search(reg, sentence):
                regex_match_list.append(fact[regex_name_index])
    for demand in RegexLib.regex_demands:
        for reg in demand[regex_index]:
            if re.search(reg, sentence):
                regex_match_list.append(demand[regex_name_index])
    for outcome in RegexLib.regex_outcomes:
        for reg in outcome[regex_index]:
            if re.search(reg, sentence):
                regex_match_list.append(outcome[regex_name_index])

    return regex_match_list


def sentence_finder(regex_name, nb_of_files):
    """
    finds sentences that matches the regex_name
    :param regex_name: name of the regex ex: landlord_money_cover_rent
    :param nb_of_files: number of files to search through
    :return: list of sentences that matched this regex
    """
    regexes = get_regexes(regex_name)
    count = 0
    regex_dict = {}

    for i in os.listdir(Path.raw_data_directory):
        if count > nb_of_files:
            break
        count += 1
        file = open(Path.raw_data_directory + i, "r", encoding="ISO-8859-1")
        for line in file:
            regex_index = 0
            for reg in regexes:
                if reg.search(line):
                    line = re.sub(r'\[\d+\]', '', line)
                    line = line.replace('"', '')
                    line = line.strip()
                    if regex_index in regex_dict.keys():
                        if line in regex_dict[regex_index]:
                            continue
                        regex_dict[regex_index].append(line)
                    else:
                        regex_dict[regex_index] = []
                regex_index += 1
        file.close()
    return regex_dict
