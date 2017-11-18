import unittest

import joblib

from feature_extraction.post_processing.models import Load
from util.constant import Global


class TestStringMethods(unittest.TestCase):
    def test_load_features(self):
        file_path = Global.ml_models_directory + 'test.bin'
        model = {'key': 'value'}
        joblib.dump(model, file_path)
        model_1 = Load.load_decisions_from_bin(file_path)
        model_2 = Load.load_facts_from_bin(file_path)
        self.assertEqual(model_1['key'], 'value')
        self.assertEqual(model_2['key'], 'value')
