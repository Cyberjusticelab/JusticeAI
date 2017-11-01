import os
import pickle

import numpy
import scipy.spatial.distance

from src.ml_service.preprocessing.French.Vectorize import FrenchVectors


# #################################################
# NAMED ENTITY
class NamedEntity:
    __fv = FrenchVectors()

    __entity = {
        0: 'Time',
        1: 'Date',
        2: 'Money',
        3: 'Time_Frequency',
        4: 'Relative_Time',
        5: 'Other'
    }

    # #################################################
    # CONSTRUCTOR
    def __init__(self):
        self.__matrix = None
        self.__load()

    # #################################################
    # LOAD
    # -------------------------------------------------
    # read .pickle model
    # create matrix
    def __load(self):
        script_dir = os.path.dirname(__file__)
        rel_path = 'ner_model.pickle'
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path, 'rb') as pickle_file:
            model = pickle.load(pickle_file)

        time_vector = model['Time']
        date_vector = model['Date']
        money_vector = model['Money']
        frequency_vector = model['Time_Frequency']
        relative_vector = model['Relative_Time']
        other_vector = model['Other']

        self.__matrix = numpy.matrix([time_vector, date_vector, money_vector,
                                      frequency_vector, relative_vector, other_vector])

    # #################################################
    # COSINE DISTANCE
    # -------------------------------------------------
    # vector: numpy array
    # return: probability matrix 1-D
    def __cos_dist(self, vector):
        v = vector.reshape(1, -1)
        return scipy.spatial.distance.cdist(self.__matrix, v, 'cosine').reshape(-1)

    # #################################################
    # MAP TO ENTITY
    # -------------------------------------------------
    # maps to a named entity
    # word_list: list[String]
    # return String
    def map_to_entity(self, word_list):
        vec = numpy.zeros(300)
        num_words = 0
        for i in range(len(word_list)):
            try:
                vec = numpy.add(vec, self.__fv.word_vectors[word_list[i]])
                num_words += 1
            except KeyError:
                if i == 0:
                    return None
                continue
        if num_words == 0:
            return 'Other'
        vec = numpy.divide(vec, num_words)
        a = self.__cos_dist(vec)
        x = numpy.where(a == numpy.min(a))
        return self.__entity[x[0][0]]
