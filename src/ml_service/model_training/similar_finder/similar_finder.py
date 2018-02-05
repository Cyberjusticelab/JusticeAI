from util.file import Save, Load
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import numpy as np


class SimilarFinder:

    def __init__(self, train=False, dataset=[]):
        """
            SimilarFinder is used to obtain the most similar cases to a given
            sample. It uses Ski-kit learn's nearest neighbor implementation
            param: train: will train the model
            param: dataset: numpy array of precedent vectors. Ignored if train
                            is set to False
        """
        if not train:
            self.model = Load.load_binary("similarity_model.bin")
            self.case_numbers = Load.load_binary("similarity_case_numbers.bin")
            self.scaler = Load.load_binary("similarity_scaler.bin")
        elif len(dataset) > 0:
            sample_set = [np.concatenate(
                [vec['facts_vector'], vec['outcomes_vector']]) for vec in dataset]

            for i in range(len(sample_set)):
                sample_set[i] = sample_set[i].astype(np.int64)

            self.scaler = StandardScaler()
            sample_set = self.scaler.fit_transform(sample_set)
            self.model = NearestNeighbors(5, metric='euclidean')
            self.model.fit(sample_set)
            self.case_numbers = [vec['name'] for vec in dataset]
            save = Save()
            save.save_binary("similarity_model.bin", self.model)
            save.save_binary("similarity_case_numbers.bin", self.case_numbers)
            save.save_binary("similarity_scaler.bin", self.scaler)
        else:
            raise ValueError('Please train or load the classifier first')

    def get_most_similar(self, sample):
        """
            Calculates the most similar cases by finding the nearest
            neighbor to the given sample
            param: sample: a Dict object with fact, demand and decision vectors
                e.g. {
                  'facts_vector' : [1,2,0..],
                  'demands_vector' : [1,2,0..],
                  'outcomes_vector' : [1,2,0..]
                }
            return: A list of tuples containing the most similar cases and their distance measure.
                    (lower is better)
                e.g. [
                  (AZ-11111, 12),
                  (AZ-12141, 5),
                  (AZ-11315, 1)
                ]
        """
        input_vector = self.scaler.transform(
            [np.concatenate([sample['facts_vector'], sample['outcomes_vector']])])
        nearest = self.model.kneighbors(input_vector)
        names = [self.case_numbers[index] for index in nearest[1][0]]
        return list(zip(names, nearest[0][0]))
