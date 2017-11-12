import unittest
from global_variables.global_variable import Global
import os

class TestStringMethods(unittest.TestCase):
    def test_init(self):
        self.assertTrue(os.path.isfile(Global.word_vector_directory + 'non-lem.bin'))
