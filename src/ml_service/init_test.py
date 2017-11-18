import os
import unittest

from util.constant import Global


class TestStringMethods(unittest.TestCase):
    def test_init(self):
        self.assertTrue(os.path.isfile(Global.word_vector_directory + 'non-lem.bin'))
