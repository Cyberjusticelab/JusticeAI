import pickle
import numpy
import scipy.spatial.distance
from src.nlp_service.preprocessing.French.Vectorize import FrenchVectors

class NamedEntity:
    fv = FrenchVectors()

    entity = {
        0: 'Time',
        1: 'Date',
        2: 'Money',
        3: 'Time_Frequency',
        4: 'Relative_Time',
        5: 'Other'
    }

    def __init__(self):
        self.matrix = None
        self.load()

    def load(self):
        with open('ner_model.pickle', 'rb') as pickle_file:
            model = pickle.load(pickle_file)
        time_vector = model['Time']
        date_vector = model['Date']
        money_vector = model['Money']
        frequency_vector = model['Time_Frequency']
        relative_vector = model['Relative_Time']
        other_vector = model['Other']
        self.matrix = numpy.matrix([time_vector, date_vector, money_vector,
                                    frequency_vector,relative_vector, other_vector])

    def cos_cdist(self, vector):
        """
        Compute the cosine distances between each row of matrix and vector.
        """
        v = vector.reshape(1, -1)
        return scipy.spatial.distance.cdist(self.matrix, v, 'cosine').reshape(-1)

    def map_to_entity(self, word_list):
        vec = numpy.zeros(300)
        num_words = 0
        for i in range(len(word_list)):
            try:
                vec = numpy.add(vec, self.fv.word_vectors[word_list[i]])
                num_words += 1
            except KeyError:
                if i == 0:
                    return None
                continue
        if num_words == 0:
            return 'Other'
        vec = numpy.divide(vec, num_words)
        a = self.cos_cdist(vec)
        x = numpy.where(a == numpy.min(a))
        return self.entity[x[0][0]]


