# -*- coding: utf-8 -*-
import pickle
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from src.nlp_service.preprocessing.French.NerMatrix import NamedEntity

class DecisionModel:
    ner = NamedEntity()
    entity_2_french = {
        'Time': "temps",
        'Date': "date",
        'Money': "argent",
        'Time_Frequency': "fréquence",
        'Relative_Time': 'relatif',
        'Other': "autre"
    }
    extra_parse = re.compile("\w'")
    custom_stop_words = stopwords.words('french') + \
                        [',', ';', '.', '!', '?',
                         'c', '(', ')']

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

    def format(self):
        for topic in self.topics:
            self.topics_str += topic + "\n"
            self.core_topic.append(self.__ner(topic))

        for fact in self.facts:
            self.facts_str += fact + "\n"
            self.core_facts.append(self.__ner(fact))

        for decision in self.decisions:
            self.decisions_str += decision + "\n"
            self.core_decisions.append(self.__ner(decision))

    def __ner(self, sentence):
        word_list = word_tokenize(sentence, language='french')
        word_list = [word for word in word_list if word not in self.custom_stop_words]
        key_lst = []
        previous_word = ''
        for i in range(len(word_list)):
            kernel = []
            kernel.append(word_list[i])
            if i != 0:
                kernel.append(word_list[i - 1])
            if i != (len(word_list) - 1):
                kernel.append(word_list[i + 1])

            entity = self.ner.map_to_entity(kernel)

            if entity == 'Other':
                key_lst.append(word_list[i])
                previous_word = word_list[i]
            elif entity is None:
                continue
            elif entity == previous_word:
                continue
            else:
                key_lst.append(self.entity_2_french[entity])
                previous_word = entity

        return key_lst

    def print_stems(self):
        print("TOPICS:")
        for topic in self.core_topic:
            print(topic)

        print("\nFACTS:")
        for fact in self.core_facts:
            print(fact)

        print("\nDECISIONS:")
        for decision in self.core_decisions:
            print(decision)

    def __str__(self):
        return "TOPICS: \n" + self.topics_str + "\n" \
               + "FACTS: \n" + self.facts_str + "\n" \
               + "DECISION: \n" + self.decisions_str

    def training_outpu(self):
        return self.topics_str + "\n" \
               + "\n" + self.facts_str + "\n" \
               + "\n" + self.decisions_str