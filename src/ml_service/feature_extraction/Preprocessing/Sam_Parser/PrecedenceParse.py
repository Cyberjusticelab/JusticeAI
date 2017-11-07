# -*- coding: utf-8 -*-
import os
import re
from sys import stdout

import numpy as np

from src.ml_service.GlobalVariables.GlobalVariable import Global
from src.ml_service.WordVectors.FrenchVectors import FrenchVectors
from src.ml_service.feature_extraction.Preprocessing.Sam_Parser.Model import PrecedenceModel
from src.ml_service.feature_extraction.Preprocessing.Sam_Parser.Pipe import PipeSent


# #################################################
# STATE
# -------------------------------------------------
# Used for state machine
# scrape text in this order:
# topic --> facts --> decision --> topic...
class State:
    TOPIC = 0
    FACTS = 1
    DECISION = 2


# #################################################
# PARSER
class Precedence_Parser:
    __factMatch = re.compile('\[\d+\]\s')
    __minimum_line_length = 6

    # #################################################
    # CONSTRUCTOR
    def __init__(self):
        self.__state = None
        self.__model = None
        self.__pipe = PipeSent()

    # #################################################
    # PARSE
    # -------------------------------------------------
    # Main method for parsing precedence
    # filename: String
    # return PrecedenceModel
    def parse(self, filename):
        self.__model = PrecedenceModel()
        self.__state = State.TOPIC
        self.__extract(filename)
        self.__model.format()
        return self.__model

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
                self.__populate_model(sentence)
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
        if 'POUR CES MOTIFS' in lines:
            self.__state = State.DECISION
        elif index is None:
            pass
        elif index == 1:
            self.__state = State.TOPIC
        elif index == 2:
            self.__state = State.FACTS

    # #################################################
    # POPULATE MODEL
    # -------------------------------------------------
    # Apppends topic, fact, decision to model
    # line: String
    def __populate_model(self, line):
        sub_sent = self.__split_sub_sentence(line)

        if self.__state == State.TOPIC:
            for i in range(len(sub_sent[0])):
                if len(sub_sent[0]) > 1:
                    self.__model.topics.append(sub_sent[0][i])
                    self.__model.original_topic.append(sub_sent[1][i])

        elif self.__state == State.FACTS:
            for i in range(len(sub_sent[0])):
                if len(sub_sent[0]) > 1:
                    self.__model.facts.append(sub_sent[0][i])
                    self.__model.original_facts.append(sub_sent[1][i])

        elif self.__state == State.DECISION:
            for i in range(len(sub_sent[0])):
                if len(sub_sent[0]) > 1:
                    self.__model.decisions.append(sub_sent[0][i])
                    self.__model.original_decisions.append(sub_sent[1][i])

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

    def parse_topics(self, file_directory, nb_of_files):
        j = 0
        data = []
        sent = []
        original_sent = []
        print("Fetching from precedence")

        for i in os.listdir(file_directory):
            if j >= nb_of_files:
                break
            j += 1

            percent = float(j / nb_of_files) * 100
            stdout.write("\rData Extraction: %f " % percent)
            stdout.flush()

            model = self.parse(i)
            for i in range(len(model.core_topic)):
                if model.topics[i] in sent:
                    continue
                vec = FrenchVectors.vectorize_sent(model.core_topic[i])
                data.append(vec)
                sent.append(model.topics[i])
                original_sent.append(model.original_topic[i])
        return np.array(data), np.array(sent), np.array(original_sent)
