# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize
from pattern3.text.fr import singularize
from nltk.corpus import stopwords
import re
import pickle
from scipy import spatial
from src.nlp_service.feature_extraction.French.Vectorize import FrenchVectors

def load():
    with open('ner_model.pickle', 'rb') as pickle_file:
        model = pickle.load(pickle_file)
    return model

class DecisionModel:
    entity_2_french = {
        'Tenant': "locataire",
        'Landlord': "locateur",
        'Time': "temps",
        'Date': "date",
        'Money': "argent",
        'Home': "habitat",
        'Lease': "bail",
        'Time_Frequency': "fréquence",
        'Article': "article",
        'Expulsion': "expulsion",
        'Termination': "résiliation",
        'Pay': "payer",
        'Order': "ordonner",
        'Compensation': "compensation",
        'Demand': "demander",
        'Reject': "rejetter",
        'Condemn': "condamner",
        'Other': "autre"
    }
    custom_vectors = load()
    fv = FrenchVectors()
    money_match = re.compile('(\d*\s*\$)')
    extra_parse = re.compile("\w'")
    custom_stop_words = stopwords.words('french') + [',', ';', '.', '!', '?', 'le', 'la', "l'", "d'", 'les', 'plus',
                                                     'dû', 'considérant', 'surtout', 'a', 'q']

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
            sent = self.__ner(topic)
            self.core_topic.append(self.__singularize(sent))

        for fact in self.facts:
            self.facts_str += fact + "\n"
            sent = self.__ner(fact)
            self.core_facts.append(self.__singularize(sent))

        for decision in self.decisions:
            self.decisions_str += decision + "\n"
            sent = self.__ner(decision)
            self.core_decisions.append(self.__singularize(sent))

    def __ner(self, sentence):
        if self.money_match.search(sentence):
            sentence = re.sub('[\d*\s*]*\$', ' argent', sentence)
        if self.extra_parse.search(sentence):
            sentence = re.sub("\w'", ' ', sentence)
        return sentence

    def __singularize(self, sentence):
        word_list = word_tokenize(sentence, language='french')
        key_lst = []
        for i in word_list:
            word = i
            if word.lower() in self.custom_stop_words:
                pass
            else:
                try:
                    self.fv.word_vectors[singularize(word)]
                except KeyError:
                    break

                for v in self.custom_vectors:
                    result = 1 - spatial.distance.cosine(self.fv.word_vectors[singularize(word)],
                                                         self.custom_vectors[v])
                    if result > 0.8:
                        word = self.entity_2_french[v]
                        break
                key_lst.append(singularize(word))
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
        return self.topics_str + "\n" \
               + "\n" + self.facts_str + "\n" \
               + "\n" + self.decisions_str
        '''
        return "TOPICS: \n" + self.topics_str + "\n" \
               + "FACTS: \n" + self.facts_str + "\n" \
               + "DECISION: \n" + self.decisions_str
        '''