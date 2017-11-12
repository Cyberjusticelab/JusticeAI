import unittest
from feature_extraction.preprocessing.precedent_parse import PrecedentParser
from word_vectors.vectors import FrenchVectors
import os
from global_variables.global_variable import Global

class TestStringMethods(unittest.TestCase):

    def test_parse_files(self):
        self.assertIsNone(FrenchVectors.word_vectors)
        __script_dir = os.path.abspath(__file__ + r"/../")
        __relative_dir = r'test/'
        __full_path = os.path.join(__script_dir, __relative_dir)
        if not os.path.exists(__full_path):
            os.makedirs(__full_path)

        file = open(__full_path + 'garbage.txt', 'w')
        file.writelines('[1] Le locateur est faible.\n')
        file.writelines('[2] Le locateur est faible.\n')
        file.writelines('[3] Le locateur est faible.\n')
        file.writelines('[4] Le locateur est faible.\n')
        file.writelines('[5] Le locateur est faible.\n')
        file.writelines('CES MOTIFS\n')
        file.writelines('[7] Le chat veut me tuer.\n')
        file.writelines('[8] Le chat veut me tuer.\n')
        file.writelines('[9] Le chat veut me tuer.\n')
        file.writelines('[10] Le chat veut me tuer.\n')
        file.close()

        Global.precedence_directory = __full_path
        parser = PrecedentParser()
        model = parser.parse_files(__full_path, 1)
        self.assertIsNone(FrenchVectors.word_vectors)
        self.assertEqual(dict, type(model))
        fact_dict = model['facts']
        decisions_dict = model['decisions']

        self.assertTrue('le locateur est faible' in fact_dict)
        self.assertTrue('le chat veut me tuer' in decisions_dict)