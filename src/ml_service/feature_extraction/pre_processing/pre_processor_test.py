import os
import unittest
import numpy
import shutil
from feature_extraction.pre_processing.pre_processor import PreProcessor
from feature_extraction.pre_processing.word_vector.french_vector import FrenchVector
from util.constant import Path


class TestStringMethods(unittest.TestCase):

    """
    1- The key to this unittest is to make sure the Word Vector model_learning
    gets its memory deallocated once we are done with it.
    2- We are also interested in separating facts from outcomes where
    we meet the string "CES MOTIFS" which appears in all the cases
    3- We expect the return type to be a dictionary
    4- The dictionary holds ["vector"] vectors, ["facts"]strings, ["filename"]strings
    """

    def test_parse_files(self):
        self.assertIsNone(FrenchVector.word_vectors)
        __script_dir = os.path.abspath(Path.cache_directory)
        __relative_dir = r"test/"
        __full_path = os.path.join(__script_dir, __relative_dir)
        if not os.path.exists(__full_path):
            os.makedirs(__full_path)

        file = open(__full_path + "garbage.txt", "w")
        file.writelines("[1] Le locateur est faible.\n")
        file.writelines("[2] Le locateur est faible.\n")
        file.writelines("[3] Le locateur est faible.\n")
        file.writelines("[4] Le locateur est faible.\n")
        file.writelines("[5] Le locateur est faible.\n")
        file.writelines("CES MOTIFS\n")
        file.writelines("[7] Le chat veut me tuer.\n")
        file.writelines("[8] Le chat veut me tuer.\n")
        file.writelines("[9] Le chat veut me tuer.\n")
        file.writelines("[10] Le chat veut me tuer.\n")
        file.close()

        Path.raw_data_directory = __full_path
        parser = PreProcessor()
        model = parser.parse_files(__full_path, 1)

        # 1
        self.assertIsNone(FrenchVector.word_vectors)

        # 2
        self.assertEqual(dict, type(model))

        fact_dict = model["facts"]
        decisions_dict = model["decisions"]

        # 3
        self.assertTrue("faible locateur" in fact_dict)
        self.assertTrue("chat tuer veut" in decisions_dict)

        # 4
        vector = decisions_dict["chat tuer veut"].dict["vector"]
        sentence = decisions_dict["chat tuer veut"].dict["fact"]
        filename = decisions_dict["chat tuer veut"].dict["precedence"]

        self.assertEqual(len(vector), FrenchVector.word_vector_size)
        sample_array = numpy.zeros(2)
        self.assertEqual(type(vector), type(sample_array))

        self.assertEqual("le chat veut me tuer", sentence)
        self.assertEqual(["garbage.txt"], filename)

        shutil.rmtree(__full_path)
