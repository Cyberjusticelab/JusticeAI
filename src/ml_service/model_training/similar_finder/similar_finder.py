from util.file import Save, Load
from sklearn.neighbors import NearestNeighbors
import numpy as np


class SimilarFinder:

    """
        SimilarFinder is used to obtain the most similar cases to a given
        sample. It uses Ski-kit learn's nearest neighbor implementation
        param: train: will train the
        param: dataset: numpy array of precedent vectors. Ignored if train
                        is set to False
    """

    def __init__(self, train=False, dataset=[]):
        if not train:
            self.model = Load.load_binary("similarity_model.bin")
            self.case_numbers = Load.load_binary("similarity_case_numbers.bin")
        elif len(dataset) > 0:
            self.model = NearestNeighbors(5, metric='mahalanobis')
            sample_set = [np.concatenate([vec['demands_vector'], vec['facts_vector'], vec[
                                         'decisions_vector']]) for vec in dataset]
            self.model.fit(sample_set)
            self.case_numbers = [vec['name'] for vec in dataset]
            save = Save()
            save.save_binary("similarity_model.bin", self.model)
            save.save_binary("similarity_case_numbers.bin", self.case_numbers)
        else:
            raise ValueError('Please train or load the classifier first')

    """
        Calculates the most similar cases by finding the nearest
        neighbor to the given sample
        param: sample: a Dict object with fact, demand and decision vectors
            e.g. {
              'facts_vector' : [1,2,0..],
              'demands_vector' : [1,2,0..],
              'decisions_vector' : [1,2,0..]
            }
        return: A list of tuples containing the most similar cases and their distance measure.
                (lower is better)
            e.g. [
              (AZ-11111, 12),
              (AZ-12141, 5),
              (AZ-11315, 1)
            ]
    """

    def get_most_similar(self, sample):
        sample_vector = np.concatenate([sample['demands_vector'], sample[
                                       'facts_vector'], sample['decisions_vector']])
        nearest = self.model.kneighbors([sample_vector])
        names = [self.case_numbers[index] for index in nearest[1][0]]
        return list(zip(names, nearest[0][0]))
