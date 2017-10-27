# -*- coding: utf-8 -*-

import re
from src.nlp_service.feature_extraction.French.Model import DecisionModel
import os

class State:
    TOPIC = 0
    FACTS = 1
    DECISION = 2


class Parser:

    factMatch = re.compile('\[\d+\]\s')
    minimum_line_length = 6

    def __init__(self):
        state = None
        model = None

    def parse(self, filename):
        self.model = DecisionModel()
        self.state = State.TOPIC
        self.__extract(filename)
        self.model.format()
        return self.model

    def __extract(self, filename):
        file = open(r'/home/charmander/Data/text_bk/' + filename, 'r', encoding="ISO-8859-1")
        for lines in file:
            tpl = self.__statement_index(lines)
            self.__update_state(tpl[1], lines)
            if self.factMatch.match(lines):
                if len(lines) < self.minimum_line_length:
                    lines = file.__next__()
                sentence = lines.replace(tpl[0], "").lower()
                sentence = sentence.replace('\n', "")
                self.__populate_model(sentence)
        file.close()

    def __statement_index(self, line):
        num = self.factMatch.match(line)
        if num is not None:
            num = num.group(0)
            index = num.replace('[', "")
            index = index.replace(']', "")
            return num, int(index)
        return None, None

    def __update_state(self, index, lines):
        if 'POUR CES MOTIFS' in lines:
            self.state = State.DECISION
        elif index is None:
            pass
        elif index == 1:
            self.state = State.TOPIC
        elif index == 2:
            self.state = State.FACTS

    def __populate_model(self, line):
        sub_sent = self.__split_sub_sentence(line)

        if self.state == State.TOPIC:
            for l in sub_sent:
                if len(l) > 1:
                    self.model.topics.append(l)

        elif self.state == State.FACTS:
            for l in sub_sent:
                if len(l) > 1:
                    self.model.facts.append(l)

        elif self.state == State.DECISION:
            for l in sub_sent:
                if len(l) > 1:
                    self.model.decisions.append(l)

    def __split_sub_sentence(self, sentence):
        sentence = sentence.replace(',', ".")
        return sentence.split('.')


if __name__ == "__main__":
    parser = Parser()
    j = 0
    for i in os.listdir(r"/home/charmander/Data/text_bk/"):
        if 'AZ-51205' in i and j < 5:
            j += 1
            model = parser.parse(i)
            model.print_stems()
