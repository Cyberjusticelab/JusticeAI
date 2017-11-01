# -*- coding: utf-8 -*-
from gensim.models.keyedvectors import KeyedVectors


def load_from_bin():
    file = r'/home/charmander/Data/french_vectors/wiki.fr.vec.bin'
    return KeyedVectors.load_word2vec_format(file, binary=True)

class FrenchVectors:
    word_vectors = load_from_bin()

    def __init__(self):
        pass

    def load_from_text(self):
        file = open(r'/home/charmander/Data/french_vectors/wiki.fr.vec', 'rb')
        self.word_vectors = KeyedVectors.load_word2vec_format(file, binary=False)
        file.close()

    def save_word_vector(self):
        file = r'/home/charmander/Data/french_vectors/wiki.fr.vec.bin'
        self.word_vectors.save_word2vec_format(file, binary = True)