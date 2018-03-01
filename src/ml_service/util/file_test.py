import unittest
from util.file import Load, Save
import os
from util.constant import Path


class TestStringMethods(unittest.TestCase):
    def test_binarize_model(self):
        binary_directory = Path.binary_directory
        Path.binary_directory = Path.test_mock_precedent_directory

        s = Save()
        model = {'key': 'value'}
        s.save_binary('test_model.bin', model)
        l = Load()
        new_model = l.load_binary('test_model.bin')
        self.assertEqual(new_model['key'], 'value')
        os.remove(Path.binary_directory + 'test_model.bin')
        Path.binary_directory = binary_directory
