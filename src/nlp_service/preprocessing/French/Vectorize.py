# -*- coding: utf-8 -*-
from gensim.models.keyedvectors import KeyedVectors
from src.nlp_service.preprocessing.French.GlobalVariable import Global

def load_from_bin():
    file = Global.Word_Vector_Directory
    return KeyedVectors.load_word2vec_format(file, binary=True)

class FrenchVectors:
    word_vectors = load_from_bin()

    def __init__(self):
        pass

    def load_from_text(self, directory):
        file = open(directory, 'rb')
        self.word_vectors = KeyedVectors.load_word2vec_format(file, binary=False)
        file.close()

    def save_word_vector(self, directory):
        file = directory
        self.word_vectors.save_word2vec_format(file, binary = True)