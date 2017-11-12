# -*- coding: utf-8 -*-
import os
import numpy
from gensim.models.keyedvectors import KeyedVectors
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from src.ml_service.word_vectors.related_word_fetcher import find_related, save_cache
from src.ml_service.outputs.output import Log


class FrenchVectors:
    word_vectors = None
    custom_stop_words = None
    Word_Vector_Size = 200

    def __init__(self):
        pass

    @staticmethod
    def load_french_vector_bin():
        """
        :return: word2vec
        """
        try:
            Log.write("Loading word vector file... May take a few seconds")
            __script_dir = os.path.abspath(__file__ + r"/../../")
            __rel_path = r'word_vectors/non-lem.bin'
            file = os.path.join(__script_dir, __rel_path)
            FrenchVectors.word_vectors = KeyedVectors.load_word2vec_format(file, binary=True)
            FrenchVectors.custom_stop_words = FrenchVectors.get_stop_words()
            Log.write("Loading complete")

        except BaseException:
            Log.write("Download French Vector model first")

    @staticmethod
    def unload_vector():
        """
        Deallocate memory
        :return: None
        """
        Log.write("Deallocating memory of word vector")
        FrenchVectors.word_vectors = None
        FrenchVectors.custom_stop_words = None
        save_cache()

    @staticmethod
    def get_stop_words():
        """
        :return: list of stopwords
        """
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

    @staticmethod
    def vectorize_sent(word_list):
        """
        Adds vectors together and divides by number of words
        :param word_list: String or list of tokenized words
        :return: Sentence vector
        """
        if not isinstance(word_list, list):
            word_list = word_tokenize(word_list, 'french')
        vector = numpy.zeros(FrenchVectors.Word_Vector_Size)
        num = 0
        for word in word_list:
            if word in FrenchVectors.custom_stop_words:
                continue
            iteration_count = 0
            max_iteration = 5
            while True:
                if iteration_count >= max_iteration:
                    break
                iteration_count += 1
                try:
                    word_vec = FrenchVectors.word_vectors[word]
                    vector = numpy.add(vector, word_vec)
                    num += 1
                    break

                except KeyError:
                    word = find_related(word)
                    if word is None:
                        break
        if num == 0:
            return vector
        return numpy.divide(vector, num)
