import unittest
from src.ml_service.feature_extraction.preprocessing.save_model import save
import joblib
import os


class TestStringMethods(unittest.TestCase):
    # to do
    def save(self):
        save('decisions', 'test.bin', 100)
        __script_dir = os.path.abspath(__file__ + r"/../")
        __processed_facts = 'processed_facts.bin'
