# -*- coding: utf-8 -*-
from src.nlp_service.feature_extraction.French.Vectorize import FrenchVectors
import os
import numpy
import pickle
import nltk
from nltk.tokenize import WhitespaceTokenizer
import re
import string

class Ner:
    entity_labels = {
        'Tenant': [],
        'Landlord': [],
        'Time': [],
        'Date': [],
        'Money': [],
        'Home': [],
        'Lease': [],
        'Time_Frequency': [],
        'Article': [],
        'Expulsion': [],
        'Termination': [],
        'Pay': [],
        'Order': [],
        'Compensation': [],
        'Demand': [],
        'Reject': [],
        'Condemn': [],
        'Other': []
    }

    def __init__(self):
        self.fv = FrenchVectors()

    def train_named_entity(self, window = 0):
        tuple_list = []
        tokens_list = []
        tokens = None
        for i in os.listdir(r"french_data/"):
            if '.ann' in i:
                text = i.split('.')[0] + '.txt'
                with open(r"french_data/" + text, 'r') as content_file:
                    content = content_file.read()
                tokens = nltk.word_tokenize(content)
                tokens_list.append(tokens)
                tpl = self.form_tuple(i)
                tuple_list.append(tpl)
                tokens = self.annotate_raw_text(content, tpl)
            self.populate_labels(tokens)
        self.define_vectors()
        self.save_pickle()

    def save_pickle(self):
        with open('ner_model.pickle', 'wb') as f:
            pickle.dump(self.entity_labels, f, pickle.HIGHEST_PROTOCOL)

    def define_vectors(self):
        for entity in self.entity_labels:
            word_lst = self.entity_labels[entity]
            num_words = 0
            vec_sum = numpy.zeros(300)
            for word in word_lst:
                word = word.lower()
                word = re.sub('['+string.punctuation+']', '', word)
                try:
                    vec_sum = numpy.add(vec_sum, self.fv.word_vectors[word])
                    num_words += 1
                except:
                    pass
            self.entity_labels[entity] = numpy.divide(vec_sum, num_words)

    def populate_labels(self, token_list):
        for token in token_list:
            try:
                self.entity_labels[token[1]].append(token[0])
            except:
                pass

    def form_tuple(self, filename):
        tuple_list = []
        file = open(r'french_data/' + filename, 'r', encoding="ISO-8859-1")
        for lines in file:
            word_ent = self.get_word_entity(lines)
            tokens = nltk.word_tokenize(word_ent[1])
            for t in tokens:
                tuple_list.append((word_ent, t))
        file.close()
        return tuple_list

    def get_word_entity(self, lines):
        line = lines.split('\t')
        entity = line[1].split(" ")
        word = line[2].replace("\n", "")
        word = word.encode("ISO-8859-1")
        word = word.decode("utf-8")
        return entity[0], word, self.get_span(entity)

    def get_span(self, entity):
        try:
            return int(entity[1]), int(entity[2])
        except:
            return int(entity[1]), int(entity[3])

    def annotate_raw_text(self, text, tuple_list):
        return_list = []
        tuple_list.sort(key=lambda x: x[0][2][0], reverse=True)
        text = text.replace(",", " ")
        for i in range(len(tuple_list)):
            span = tuple_list[i][0][2]
            start = span[0]
            end = span[1]
            try:
                if text[start + 1] == "(":
                    continue
                elif text[start] == "(":
                    continue
            except IndexError:
                pass
            text = text[:end] + ';' + tuple_list[i][0][0] + ")" + text[end:]
            text = text[:start] + "(" + text[start:]
        text = text.replace("'", " ")
        text = text.replace("\n", " ")
        tokens = text.split(" ")
        for i in range(len(tokens)):
            if tokens[i] == "":
                pass
            elif tokens[i][0] == '(':
                tokens[i] = tokens[i].replace("(", "")
                tokens[i] = tokens[i].replace(")", "")
                tpl = tokens[i].split(';')
                try:
                    return_list.append((tpl[0], tpl[1]))
                except:
                    pass
            else:
                return_list.append((tokens[i], 'Other'))
        return return_list

ner = Ner()
ner.train_named_entity()

