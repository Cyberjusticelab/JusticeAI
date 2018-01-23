import os
import unittest
import joblib
import numpy

from feature_extraction.pre_processing.pre_processing_driver import run
from util.constant import Path


class TestPreProcessingMethods(unittest.TestCase):

    def test_save(self):
        facts = "test_facts"

        raw_data_directory = Path.raw_data_directory
        Path.precedent_directory = Path.test_data_directory
        file = open(Path.test_data_directory + "garbage.txt", "w")
        file.writelines("[1] Le locateur est faible.\n")
        file.writelines("[2] Le locateur est faible.\n")
        file.writelines("[3] Le locateur est faible.\n")
        file.writelines("[4] Le locateur est faible.\n")
        file.writelines("[5] Le locateur est faible.\n")
        file.writelines("[6] Le chat veut me tuer.\n")
        file.writelines("[7] Le chat veut me tuer.\n")
        file.writelines("[8] Le chat veut me tuer.\n")
        file.writelines("[9] Le chat veut me tuer.\n")
        file.writelines("[10] Le chat veut me tuer.\n")
        file.close()
        run([1], facts)

        binary_model_path = Path.binary_directory + "test_facts.bin"
        self.assertTrue(os.path.isfile(binary_model_path))

        model = joblib.load(binary_model_path)
        sample_matrix = numpy.matrix([2, 1])
        sample_array = numpy.zeros(2)

        self.assertEqual(type(model[0]), type(sample_matrix))
        self.assertEqual(type(model[1]), type(sample_array))
        self.assertEqual(type(model[2]), type(sample_array))

        os.remove(binary_model_path)
        os.remove(Path.test_data_directory + 'garbage.txt')
        Path.raw_data_directory = raw_data_directory