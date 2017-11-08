# -*- coding: utf-8 -*-
import numpy
import os
import pickle
from gensim.models.keyedvectors import KeyedVectors
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from src.ml_service.feature_extraction.Preprocessing.Arek_Parser.related_word_fetcher import find_related


# #################################################
# LOAD FROM .bin
# -------------------------------------------------
# return word_vector_model
def load_from_bin():
    try:
        print("Loading word vector file... May take a few seconds")
        __script_dir = os.path.abspath(__file__ + r"/../../")
        __rel_path = r'WordVectors/non-lem.bin'
        file = os.path.join(__script_dir, __rel_path)
        model = KeyedVectors.load_word2vec_format(file, binary=True)
        print("Loading complete")
        return model
    except BaseException:
        print("Download French Vector model first")


def load_tf_idf_from_bin():
    try:
        print("Loading tf-idf file... May take a few seconds")
        __script_dir = os.path.abspath(__file__ + r"/../../")
        __rel_path = r'WordVectors/feature_idf.bin'
        file_path = os.path.join(__script_dir, __rel_path)
        file = open(file_path, 'rb')
        model = pickle.load(file)
        print("Loading complete")
        return model
    except BaseException:
        print("Download tf-idf binary first")


def get_stop_words():
    return stopwords.words('french') + \
        [',', ';', '.', '!', '?', 'c', '(', ')', 'ainsi',
            'alors', 'au', 'aucuns', 'aussi', 'autre', 'avant', 'avec',
            'avoir', 'bon', 'car', 'ce', 'cela', 'ces', 'ceux',
            'chaque', 'ci', 'comme', 'comment', 'dans', 'des', 'du', 'dedans',
            'dehors', 'depuis', 'devrait', 'doit', 'donc', 'dos', 'début',
            'elle', 'elles', 'en', 'encore', 'essai', 'est', 'et', 'eu', 'fait',
            'faites', 'fois', 'font', 'hors', 'ici', 'il', 'ils', 'la', 'le', 'les',
            'leur', 'là', 'ma', 'maintenant', 'mais', 'mes', 'mine', 'moins',
            'mon', 'mot', 'même', 'ni', 'nommés', 'notre', 'nous', 'ou',
            'où', 'par', 'parce', 'pas', 'peut', 'peu', 'plupart', 'pour',
            'pourquoi', 'quand', 'que', 'quel', 'quelle', 'quelles', 'quels',
            'qui', 'sa', 'sans', 'ses', 'seulement', 'si', 'sien', 'son', 'sont',
            'sous', 'soyez', 'sur', 'ta', 'tandis', 'tellement', 'tels',
            'tes', 'ton', 'tous', 'tout', 'trop', 'très', 'tu', 'voient',
            'vont', 'votre', 'vous', 'vu', 'ça', 'étaient', 'état', 'étions', 'été', 'être',
         ]


class FrenchVectors:
    word_vectors = load_from_bin()
    custom_stop_words = get_stop_words()
    Word_Vector_Size = 500
    word_idf_dict = None

    def __init__(self):
        pass

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
        if type(word_list) is not list:
            word_list = word_tokenize(word_list, 'french')
        vector = numpy.zeros(FrenchVectors.Word_Vector_Size)
        num = 0
        for word in word_list:
            if word in FrenchVectors.custom_stop_words:
                continue
            while True:
                try:
                    word_vec = FrenchVectors.word_vectors[word]
                    if FrenchVectors.word_idf_dict is not None:
                        word_idf = FrenchVectors.word_idf_dict[word]
                        if word_idf is not None:
                            word_vec = numpy.multiply(word_idf, word_vec)
                    vector = numpy.add(vector, word_vec)
                    num += 1
                    break

                except KeyError:
                    word = find_related(word)
                    if word is None:
                        break
        if num == 0:
            return None
        return numpy.divide(vector, num)
