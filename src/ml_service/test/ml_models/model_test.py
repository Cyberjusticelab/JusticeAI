import unittest
from src.ml_service.ml_models.models import Load
import joblib
import os


class TestStringMethods(unittest.TestCase):
    def test_load_features(self):
        __script_dir = os.path.abspath(__file__ + r"/../../../")
        __processed_facts = 'ml_models/test.bin'
        file_path = os.path.join(__script_dir, __processed_facts)
        model = {'key': 'value'}
        joblib.dump(model, file_path)
        model_1 = Load.load_decisions_from_bin(file_path)
        model_2 = Load.load_facts_from_bin(file_path)
        self.assertEqual(model_1['key'], 'value')
        self.assertEqual(model_2['key'], 'value')
