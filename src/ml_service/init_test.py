import unittest
from src.ml_service.global_variables.global_variable import Global
import os
from src.ml_service import init

class TestStringMethods(unittest.TestCase):
    def test_init(self):
        self.assertTrue(os.path.isfile(Global.word_vector_directory + 'non-lem.bin'))
