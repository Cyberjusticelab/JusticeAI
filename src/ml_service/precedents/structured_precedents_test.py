import unittest
import numpy
from hdbscan import HDBSCAN
from precedents.structured_precedents import StructuredPrecedent


class StructuredPrecedentsTest(unittest.TestCase):
    def create_structure_from_data_tuple_test(self):
        matrix = numpy.matrix([[2, 3, 4, 5], [2, 1, 6, 7], [2, 54, 12, 23],[2, 3, 4, 5], [2, 1, 6, 7], [2, 54, 12, 23],[2, 3, 4, 5], [2, 1, 6, 7], [2, 54, 12, 23]])
        sentence = numpy.array([['I shot the supremacist.'], ['Over 9000'], ['Bruce lee'],['I shot the supremacist.'],['Over 9000'], ['Bruce lee'], ['I shot the supremacist.'], ['Over 9000'], ['Bruce lee']])
        files = numpy.array([['1'], ['2'], ['3'], ['1'], ['2'], ['3'], ['1'], ['2'], ['3']])
        data_tuple = (matrix, sentence, files)
        hdb = HDBSCAN(min_cluster_size=2, min_samples=1).fit(data_tuple[0])
        precedents = StructuredPrecedent(hdb.labels_, data_tuple, hdb.labels_, data_tuple)
        self.assertEqual(precedents.precedents['1']['decisions_vector'][0], 0)
        self.assertEqual(precedents.precedents['1']['decisions_vector'][1], 1)
        self.assertEqual(precedents.precedents['1']['decisions_vector'][2], 0)
