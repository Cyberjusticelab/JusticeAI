# -*- coding: utf-8 -*-
import os
import re
from sys import stdout
from src.ml_service.GlobalVariables.GlobalVariable import Global
from src.ml_service.WordVectors.FrenchVectors import FrenchVectors
from src.ml_service.feature_extraction.Preprocessing.Sam_Parser.Model import PrecedenceModel, FactModel
from src.ml_service.feature_extraction.Preprocessing.Sam_Parser.Pipe import PipeSent


# #################################################
# STATE
# -------------------------------------------------
# Used for state machine
# scrape text in this order:
# topic --> facts --> decision --> topic...
class State:
    FACTS = 1
    DECISION = 2


# #################################################
# PARSER
class Precedence_Parser:
    __factMatch = re.compile('\[\d+\]\s')
    __minimum_line_length = 6

    # #################################################
    # CONSTRUCTOR
    def __init__(self, tfidf=False):
        if tfidf:
            FrenchVectors.word_idf_dict = FrenchVectors.load_tf_idf_from_bin()
        self.__state = None
        self.__model = None
        self.__filename = None
        self.__model = PrecedenceModel()
        self.__pipe = PipeSent()

    # #################################################
    # PARSE
    # -------------------------------------------------
    # Main method for parsing precedence
    # filename: String
    # return PrecedenceModel
    def __parse(self, filename):
        self.__filename = filename
        self.__state = State.FACTS
        self.__extract(filename)

    # #################################################
    # EXTRACT
    # -------------------------------------------------
    # Extract every line from the precedence that start
    # with [<number>]
    # filename: String
    def __extract(self, filename):
        file = open(Global.Precedence_Directory + filename, 'r', encoding="ISO-8859-1")
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

    # #################################################
    # STATEMENT INDEX
    # -------------------------------------------------
    # Keep track of the index of the statement we
    # are currently reading.
    # Used to reset state machine if index goes back
    # to 1
    # line: String
    # return: (string, int)
    def __statement_index(self, line):
        num = self.__factMatch.match(line)
        if num is not None:
            num = num.group(0)
            index = num.replace('[', "")
            index = index.replace(']', "")
            return num, int(index)
        return None, None

    # #################################################
    # UPDATE STATE
    def __update_state(self, index, lines):
        if 'CES MOTIFS' in lines:
            self.__state = State.DECISION
        elif index is None:
            pass
        elif index == 1:
            self.__state = State.FACTS

    # #################################################
    # POPULATE MODEL
    # -------------------------------------------------
    # Apppends topic, fact, decision to model
    # line: String
    def __add_key(self, line):
        # subsent is a tuple
        # (list<original sentence>, <processed sub sentence)>
        sub_sent = self.__split_sub_sentence(line)

        if self.__state == State.FACTS:
            dict = self.__model.dict['facts']

        elif self.__state == State.DECISION:
            dict = self.__model.dict['decisions']

        for i in range(len(sub_sent[0])):
            if sub_sent[0][i] in self.__model.dict:
                dict['precedence'].append(self.__filename)
            else:
                fact_model = FactModel()
                new_dict = fact_model.dict
                new_dict['fact'] = sub_sent[1][i]
                new_dict['piped_fact'] = sub_sent[0][i]
                new_dict['precedence'].append(self.__filename)
                new_dict['vector'] = FrenchVectors.vectorize_sent(sub_sent[0][i])
                dict[sub_sent[1][i]] = fact_model

    # #################################################
    # SPLIT SUB SENTENCE
    # -------------------------------------------------
    # Splits sentence where a ',' or a '.' is found.
    # ** This method can be enhanced for better classification
    #    This is just a proof of concept for now
    def __split_sub_sentence(self, sentence):
        sent_list = sentence.split('.')
        sub_sent = []
        original_sent = []
        for sent in sent_list:
            try:
                tpl = self.__pipe.pipe(sent)
                sub_sent += tpl[0]
                original_sent += tpl[1]
            except TypeError:
                pass
        return sub_sent, original_sent

    '''
    ------------------------------------------------------
    Parse Training Data
    ------------------------------------------------------

    Vectorizes sentences and creates a matrix from it.
    Also appends original sentence to a list

    file_directory <string>: precedence file directory
    nb_of_files <int>: Number of files to train on

    returns <array, array, array>
    '''

    def parse_files(self, file_directory, nb_of_files):
        files_parse = 0
        print("Fetching from precedence")

        for i in os.listdir(file_directory):
            if files_parse >= nb_of_files:
                break
            files_parse += 1

            percent = float(files_parse / nb_of_files) * 100
            stdout.write("\rData Extraction: %.2f%%" % percent)
            stdout.flush()

            self.__parse(i)
        return self.__model.dict


if __name__ == '__main__':
    parser = Precedence_Parser()
    precedence_dict = parser.parse_files(Global.Precedence_Directory, 10)
    print(precedence_dict)
