import os
import unittest
import joblib
from util.file import Load, Save
from util.constant import Path
import numpy


class TestStringMethods(unittest.TestCase):

    def test_binarize_model(self):
        s = Save()
        model = {'key': 'value'}
        s.save_binary('test_model.bin', model)
        l = Load()
        new_model = l.load_binary('test_model.bin')
        self.assertEqual(new_model['key'], 'value')
