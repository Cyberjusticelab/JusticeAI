import os
import unittest

import joblib
import numpy

from feature_extraction.pre_processing.save_model import save
from util.constant import Global


class TestStringMethods(unittest.TestCase):

    def test_save(self):
        __script_dir = os.path.abspath(__file__ + r"/../")
        __relative_dir = r'test/'
        __full_path = os.path.join(__script_dir, __relative_dir)
        if not os.path.exists(__full_path):
            os.makedirs(__full_path)
        facts = 'test_facts'

        Global.precedent_directory = __full_path
        file = open(__full_path + 'garbage.txt', 'w')
        file.writelines('[1] Le locateur est faible.\n')
        file.writelines('[2] Le locateur est faible.\n')
        file.writelines('[3] Le locateur est faible.\n')
        file.writelines('[4] Le locateur est faible.\n')
        file.writelines('[5] Le locateur est faible.\n')
        file.writelines('[6] Le chat veut me tuer.\n')
        file.writelines('[7] Le chat veut me tuer.\n')
        file.writelines('[8] Le chat veut me tuer.\n')
        file.writelines('[9] Le chat veut me tuer.\n')
        file.writelines('[10] Le chat veut me tuer.\n')
        file.close()
        save(facts, 1)

        binary_model_path = Global.output_directory + 'preprocess_model/test_facts.bin'
        self.assertTrue(os.path.isfile(binary_model_path))

        model = joblib.load(binary_model_path)
        sample_matrix = numpy.matrix([2, 1])
        sample_array = numpy.zeros(2)

        self.assertEqual(type(model[0]), type(sample_matrix))
        self.assertEqual(type(model[1]), type(sample_array))
        self.assertEqual(type(model[2]), type(sample_array))
