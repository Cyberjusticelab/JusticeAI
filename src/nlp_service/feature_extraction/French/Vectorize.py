# -*- coding: utf-8 -*-
from gensim.models.keyedvectors import KeyedVectors

class FrenchVectors:
    def __init__(self):
        file = open(r'/home/charmander/Data/french_vectors/wiki.fr.vec', 'rb')
        self.word_vectors = KeyedVectors.load_word2vec_format(file)
        file.close()

