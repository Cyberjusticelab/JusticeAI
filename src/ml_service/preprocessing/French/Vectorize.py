# -*- coding: utf-8 -*-
from gensim.models.keyedvectors import KeyedVectors

from src.ml_service.preprocessing.French.GlobalVariable import Global


# #################################################
# LOAD FROM .bin
# -------------------------------------------------
# return word_vector_model
def load_from_bin():
    print("Loading word vector file... May take a few seconds")
    file = Global.Word_Vector_Directory
    model = KeyedVectors.load_word2vec_format(file, binary=True)
    print("Loading complete")
    return model


class FrenchVectors:
    word_vectors = load_from_bin()

    def __init__(self):
        pass

    # #################################################
    # LOAD FROM TEXT
    # -------------------------------------------------
    # return word_vector_model
    def load_from_text(self, directory):
        file = open(directory, 'rb')
        self.word_vectors = KeyedVectors.load_word2vec_format(file, binary=False)
        file.close()

    # #################################################
    # SAVE VECTOR
    def save_word_vector(self, directory):
        file = directory
        self.word_vectors.save_word2vec_format(file, binary=True)
