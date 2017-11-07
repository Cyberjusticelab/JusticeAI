# -*- coding: utf-8 -*-
import re

from nltk.tokenize import word_tokenize

from src.ml_service.WordVectors.FrenchVectors import FrenchVectors

# #################################################
# PRECEDENCE MODEL


class PrecedenceModel:
    extra_parse = re.compile("l'")

    # English named entities to french
    entity_2_french = {
        'Time': "temps",
        'Date': "date",
        'Money': "argent",
        'Time_Frequency': "fréquence",
        'Relative_Time': 'relatif',
        'Other': "autre"
    }

    syn_dict = {
        'locateur': 'propriétaire',
        'locatrice': 'propriétaire'
    }

    # #################################################
    # CONSTRUCTOR
    def __init__(self):
        self.topics = []
        self.facts = []
        self.decisions = []

        self.topics_str = ""
        self.facts_str = ""
        self.decisions_str = ""

        self.core_topic = []
        self.core_facts = []
        self.core_decisions = []

        self.original_topic = []
        self.original_facts = []
        self.original_decisions = []

    # #################################################
    # FORMAT
    # -------------------------------------------------
    # Filtering process of key phrases
    def format(self):
        for topic in self.topics:
            self.topics_str += topic + "\n"
            lst = self.__replace(topic)
            if len(lst) > 0:
                self.core_topic.append(lst)

        for fact in self.facts:
            self.facts_str += fact + "\n"
            lst = self.__replace(fact)
            if len(lst) > 0:
                self.core_facts.append(lst)

        for decision in self.decisions:
            self.decisions_str += decision + "\n"
            lst = self.__replace(decision)
            if len(lst) > 0:
                self.core_decisions.append(lst)

    # #################################################
    # NAMED ENTITY RECOGNITION
    # -------------------------------------------------
    # maps every word to a ner
    # uses word window = 1 by default. Only configuration
    # that gave good results
    # sentence: String
    # return: list[String]
    def __replace(self, sentence):
        word_list = self.__preprocess(sentence)
        for i in range(len(word_list)):
            try:
                word_list[i] = self.syn_dict[word_list[i]]
            except KeyError:
                pass
        return word_list

    # #################################################
    #
    def __preprocess(self, sentence):
        if self.extra_parse.search(sentence):
            sentence = re.sub("l'", ' ', sentence)

        word_list = word_tokenize(sentence, language='french')
        word_list = [word for word in word_list if word not in FrenchVectors.custom_stop_words]
        return word_list

    # #################################################
    # PRINT NER
    def print_ner(self):
        print("TOPICS:")
        for topic in self.core_topic:
            print(topic)

        print("\nFACTS:")
        for fact in self.core_facts:
            print(fact)

        print("\nDECISIONS:")
        for decision in self.core_decisions:
            print(decision)

    # #################################################
    # TRAINING OUTPUT
    # -------------------------------------------------
    # Use this method to read text if you want to create
    # a corpus.
    # copy paste text output to your text editor/corpus
    def training_output(self):
        out = self.topics_str + "\n"
        out += "\n" + self.facts_str + "\n"
        out += "\n" + self.decisions_str
        return out

    def __str__(self):
        out = "TOPICS: \n" + self.topics_str + "\n"
        out += "FACTS: \n" + self.facts_str + "\n"
        out += "DECISION: \n" + self.decisions_str
        return out
