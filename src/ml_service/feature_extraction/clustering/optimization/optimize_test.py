import unittest
from feature_extraction.clustering.optimization.optimize import epsilon_histogram, cluster_size_histogram
import numpy


class TestStringMethods(unittest.TestCase):
    def test_epsilon_histogram(self):
        matrix = numpy.matrix([[2, 3, 4, 5], [2, 1, 6, 7], [2, 54, 12, 23]])
        hist = epsilon_histogram(matrix)
        self.assertEqual(dict, type(hist))
        epsilon = list(hist.keys())
        density = list(hist.values())
        epsilon_list = ['3.5', '54.7']
        print(epsilon)
        print(epsilon_list)
        density_list = [2, 1]
        self.assertEqual(epsilon, epsilon_list)
        self.assertEqual(density, density_list)

    def test_cluster_size_histogram(self):
        matrix = numpy.matrix([[2, 3, 4, 5], [2, 1, 6, 7], [2, 54, 12, 23]])
        hist = cluster_size_histogram(matrix, 0.1)
        self.assertEqual(dict, type(hist))
        cluster_size = list(hist.keys())
        density = list(hist.values())
        cluster_list = [1]
        density_list = [3]
        self.assertEqual(cluster_size, cluster_list)
        self.assertEqual(density, density_list)