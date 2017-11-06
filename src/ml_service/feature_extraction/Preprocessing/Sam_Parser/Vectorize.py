# -*- coding: utf-8 -*-
import numpy
from gensim.models.keyedvectors import KeyedVectors

from src.ml_service.GlobalVariables.GlobalVariable import Global


# #################################################
# LOAD FROM .bin
# -------------------------------------------------
# return word_vector_model
def load_from_bin():
    try:
        print("Loading word vector file... May take a few seconds")
        file = Global.French_Word_Vector_Directory
        model = KeyedVectors.load_word2vec_format(file, binary=True)
        print("Loading complete")
        return model
    except BaseException:
        return None


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

    '''
    ----------------------------------------------------------------
    Vectorize Sentence
    ----------------------------------------------------------------
    
    Adds vectors together and divides by number of words
    
    word_list <list[String]>: list of words representing a sentence
    return: numpy array
    '''
    @staticmethod
    def vectorize_sent(word_list):
        vector = numpy.zeros(Global.Word_Vector_Size)
        num = 0
        for word in word_list:
            try:
                if word in Global.custom_stop_words:
                    continue
                vector = numpy.add(vector, FrenchVectors.word_vectors[word])
                num += 1
            except KeyError:
                pass
        return numpy.divide(vector, num)

    '''
    ---------------------------------------------------
    Vectorize Kernel
    ---------------------------------------------------
    
    Vectorizes word window given by the kernel matrix.
    Used in named entity recognition
    
    word_list: <list[String]>
    returns: numpy array
    '''
    @staticmethod
    def vectorize_kernel(word_list):
        vec = numpy.zeros(Global.Word_Vector_Size)
        num_words = 0
        for i in range(len(word_list)):
            try:
                if word_list[i] in Global.custom_stop_words:
                    continue
                vec = numpy.add(vec, FrenchVectors.word_vectors[word_list[i]])
                num_words += 1
            except KeyError:
                if i == 0:
                    return None
                continue
        if num_words == 0:
            return None
        return numpy.divide(vec, num_words)
