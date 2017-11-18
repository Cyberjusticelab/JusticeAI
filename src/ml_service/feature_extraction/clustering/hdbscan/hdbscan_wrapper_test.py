import unittest

import numpy

from feature_extraction.clustering.hdbscan.hdbscan_wrapper import HdbscanTrain
from util.constant import Global


class TestStringMethods(unittest.TestCase):
    def test_hdbscan(self):
        matrix = numpy.matrix([[2, 3, 4, 5], [2, 1, 6, 7], [2, 54, 12, 23]])
        sentence = numpy.array([["I shot the supremacist."], ["Over 9000"], ["Bruce lee"]])
        files = numpy.array([["1"], ["2"], ["3"]])
        data_tuple = (matrix, sentence, files)
        hdb = HdbscanTrain()
        hdb.cluster(data_tuple, 2, 1)
        expected_cluster = """I shot the supremacist.\nOver 9000\nBruce lee\n\n------------------------------------------\n\n1\n2\n3\n"""
        file = Global.output_directory + r"/hdb_cluster_dir/-1.txt"
        text = ""
        file = open(file, "r")
        for lines in file:
            text += lines
        file.close()
        self.assertEqual(text, expected_cluster)
