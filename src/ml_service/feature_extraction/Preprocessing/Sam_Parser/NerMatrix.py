import os
import pickle

import numpy
import scipy.spatial.distance

from src.ml_service.feature_extraction.Preprocessing.Sam_Parser.Vectorize import FrenchVectors
from src.ml_service.GlobalVariables.GlobalVariable import Global


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
        with open(Global.French_NER, 'rb') as pickle_file:
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
        vec = FrenchVectors.vectorize_kernel(word_list)
        if vec is None:
            return None
        a = self.__cos_dist(vec)
        x = numpy.where(a == numpy.min(a))
        return self.__entity[x[0][0]]
