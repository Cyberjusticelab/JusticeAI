# -*- coding: utf-8 -*-
import re

from src.nlp_service.preprocessing.French.GlobalVariable import Global
from src.nlp_service.preprocessing.French.Model import PrecedenceModel


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
class Parser:
    __factMatch = re.compile('\[\d+\]\s')
    __minimum_line_length = 6

    # #################################################
    # CONSTRUCTOR
    def __init__(self):
        self.__state = None
        self.__model = None

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
            for l in sub_sent:
                if len(l) > 1:
                    self.__model.topics.append(l)

        elif self.__state == State.FACTS:
            for l in sub_sent:
                if len(l) > 1:
                    self.__model.facts.append(l)

        elif self.__state == State.DECISION:
            for l in sub_sent:
                if len(l) > 1:
                    self.__model.decisions.append(l)

    # #################################################
    # SPLIT SUB SENTENCE
    # -------------------------------------------------
    # Splits sentence where a ',' or a '.' is found.
    # ** This method can be enhanced for better classification
    #    This is just a proof of concept for now
    def __split_sub_sentence(self, sentence):
        sentence = sentence.replace(',', ".")
        return sentence.split('.')
