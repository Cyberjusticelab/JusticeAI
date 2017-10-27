# -*- coding: utf-8 -*-
from src.nlp_service.feature_extraction.French.Vectorize import FrenchVectors
import os
import numpy
import json
import pickle


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
        fv = FrenchVectors()

    def parse_named_entity(self):
        tuple_list = []
        for i in os.listdir(r"french_data/"):
            if '.ann' in i:
                tuple_list += self.form_tuple(i)
        self.populate_labels(tuple_list)
        self.define_vectors()
        self.save_pickle()

    #####################################
    # SAVE PICKLE
    def save_pickle(self):
        with open('ner_model.pickle', 'wb') as f:
            pickle.dump(self.entity_labels, f, pickle.HIGHEST_PROTOCOL)

    def define_vectors(self):
        for entity in self.entity_labels:
            vec_lst = self.entity_labels[entity]
            num_words = 0
            vec_sum = numpy.zeros(300)
            for vec in vec_lst:
                vec_sum = numpy.add(vec_sum, vec)
                num_words += 1
            self.entity_labels[entity] = numpy.divide(vec_sum, num_words)

    def populate_labels(self, train_data):
        for t in train_data:
            words = t[1].split(" ")
            for w in words:
                try:
                    self.entity_labels[t[0]].append(self.fv.word_vectors[w])
                except KeyError:
                    pass

    def form_tuple(self, filename):
        tuple_list = []
        file = open(r'french_data/' + filename, 'r', encoding="ISO-8859-1")
        for lines in file:
            line = lines.split('\t')
            element = line[1].split(" ")
            word = line[2].replace("\n", "")
            # Pure cancer
            word = word.encode("ISO-8859-1")
            word = word.decode("utf-8")
            tuple_list.append((element[0], word))
        file.close()
        return tuple_list

ner = Ner()
ner.parse_named_entity()

