from nltk.tokenize import word_tokenize
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords
import re


class DecisionModel:
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
            self.core_topic.append(self.__stem(sent))

        for fact in self.facts:
            self.facts_str += fact + "\n"
            sent = self.__ner(fact)
            self.core_facts.append(self.__stem(sent))

        for decision in self.decisions:
            self.decisions_str += decision + "\n"
            sent = self.__ner(decision)
            self.core_decisions.append(self.__stem(sent))

    def __ner(self, sentence):
        if self.money_match.search(sentence):
            sentence = re.sub('[\d*\s*]*\$', ' argent', sentence)
        if self.extra_parse.search(sentence):
            sentence = re.sub("\w'", ' ', sentence)
        return sentence

    def __stem(self, sentence):
        word_list = word_tokenize(sentence, language='french')
        stemmer = FrenchStemmer()
        key_lst = []
        for i in word_list:
            if i.lower() in self.custom_stop_words:
                pass
            else:
                key_lst.append(stemmer.stem(i))
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