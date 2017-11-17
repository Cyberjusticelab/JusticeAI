import unittest
from feature_extraction.preprocessing.precedent_parse import PrecedentParser
from word_vectors.vectors import FrenchVectors
import os
from global_variables.global_variable import Global
import numpy


class TestStringMethods(unittest.TestCase):

    """
    1- The key to this unittest is to make sure the Word Vector model
    gets its memory deallocated once we are done with it.
    2- We are also interested in separating facts from outcomes where
    we meet the string 'CES MOTIFS' which appears in all the cases
    3- We expect the return type to be a dictionary
    4- The dictionary holds ['vector'] vectors, ['facts']strings, ['filename']strings
    """

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

        # 1
        self.assertIsNone(FrenchVectors.word_vectors)

        # 2
        self.assertEqual(dict, type(model))

        fact_dict = model['facts']
        decisions_dict = model['decisions']

        # 3
        self.assertTrue('faible locateur' in fact_dict)
        self.assertTrue('chat tuer veut' in decisions_dict)

        # 4
        vector = decisions_dict['chat tuer veut'].dict['vector']
        sentence = decisions_dict['chat tuer veut'].dict['fact']
        filename = decisions_dict['chat tuer veut'].dict['precedence']

        self.assertEqual(len(vector), FrenchVectors.Word_Vector_Size)
        sample_array = numpy.zeros(2)
        self.assertEqual(type(vector), type(sample_array))

        self.assertEqual('le chat veut me tuer', sentence)
        self.assertEqual(['garbage.txt'], filename)
