import os
import unittest
from util.constant import Path

class TestStringMethods(unittest.TestCase):
    def test_init(self):
        import init
        self.assertTrue(os.path.isfile(Path.binary_directory + 'non-lem.bin'))
