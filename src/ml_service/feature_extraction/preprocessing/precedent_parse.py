# -*- coding: utf-8 -*-
import os
import re
from sys import stdout
from feature_extraction.preprocessing.precedent_model import PrecedentModel, FactModel
from global_variables.global_variable import Global
from outputs.output import Log
from word_vectors.vectors import FrenchVectors

class State:
    """
    Used for state machine
    scrape text in this order:
    facts --> decision --> facts...
    """
    FACTS = 1
    DECISION = 2


# #################################################
# PARSER
class PrecedentParser:
    __factMatch = re.compile('\[\d+\]\s')
    __minimum_line_length = 6

    def __init__(self):
        self.__state = None
        self.__filename = None
        self.__model = PrecedentModel()

    def __parse(self, filename):
        """
        Main method for parsing precedence
        :param filename: String
        :return: None
        """
        self.__filename = filename
        self.__state = State.FACTS
        self.__extract(filename)

    def __extract(self, filename):
        """
        Extract every line from the precedence that start
        with [<number>]
        :param filename: String
        :return: None
        """
        file = open(Global.precedence_directory + filename, 'r', encoding="ISO-8859-1")
        for lines in file:
            tpl = self.__statement_index(lines)
            self.__update_state(tpl[1], lines)
            if self.__factMatch.match(lines):
                if len(lines) < self.__minimum_line_length:
                    lines = file.__next__()
                sentence = lines.replace(tpl[0], "").lower()
                sentence = sentence.replace('\n', "")
                self.__add_key(sentence)
        file.close()

    def __statement_index(self, line):
        """
        Keep track of the index of the statement we
        are currently reading.
        Used to reset state machine if index goes back to 1
        :param line: String
        :return: (String, int)
        """
        num = self.__factMatch.match(line)
        if num is not None:
            num = num.group(0)
            index = num.replace('[', "")
            index = index.replace(']', "")
            return num, int(index)
        return None, None

    def __update_state(self, index, lines):
        """
        Attempts to update state machine
        :param index: int
        :param lines: String
        :return: None
        """
        if 'CES MOTIFS' in lines:
            self.__state = State.DECISION
        elif index is None:
            pass
        elif index == 1:
            self.__state = State.FACTS

    def __add_key(self, line):
        """
        Apppends fact<strings> and decision<strings> to model
        1 - Splits sentence where it finds a '.'
        2 - Fetch dictionary based on state machine
        3 - If key already exist in dictionary then simply append filename
        4 - If key doesn't exist then create a new model and insert it
        :param line: String
        :return: None
        """
        sub_sent_list = self.__split_sub_sentence(line)

        if self.__state == State.FACTS:
            dict = self.__model.dict['facts']

        elif self.__state == State.DECISION:
            dict = self.__model.dict['decisions']

        for sub_sent in sub_sent_list:
            if sub_sent in self.__model.dict:
                if self.__filename not in dict['precedence']:
                    dict['precedence'].append(self.__filename)
            else:
                fact_model = FactModel()
                new_dict = fact_model.dict
                new_dict['fact'] = sub_sent
                new_dict['precedence'].append(self.__filename)
                new_dict['vector'] = FrenchVectors.vectorize_sent(sub_sent)
                dict[sub_sent] = fact_model

    def __split_sub_sentence(self, sentence):
        """
        Splits sentence where a '.' is found.
        This method can be enhanced for better classification
        This is just a proof of concept for now
        :param sentence: String
        :return: list[Strings]
        """
        sub_sent_list = sentence.split('.')
        return sub_sent_list

    def parse_files(self, file_directory, nb_of_files=-1):
        """
        Vectorizes sentences and creates a matrix from it.
        Also appends original sentence to a list

        :param file_directory: String
        :param nb_of_files: int.
               -1 indicates to read entire directory
        :return: Dictionary
        """
        FrenchVectors.load_french_vector_bin()
        files_parse = 0
        Log.write("Fetching from precedence")
        for i in os.listdir(file_directory):
            if (files_parse >= nb_of_files) and (nb_of_files > -1):
                break
            files_parse += 1
            percent = float(files_parse / nb_of_files) * 100
            stdout.write("\rData Extraction: %f " % percent)
            stdout.flush()
            self.__parse(i)
        print()
        # deallocate memory
        FrenchVectors.unload_vector()
        return self.__model.dict
