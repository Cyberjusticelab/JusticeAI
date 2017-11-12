import os
import unittest

from rasa.rasa_classifier import RasaClassifier


class TestRasaClassifier(unittest.TestCase):
    def setUp(self):
        self.rasaClassifier = RasaClassifier()
        self.rasaClassifier.train(force_train=True)

    def test_rasaclassifier_should_instantiate(self):
        self.assertIsNotNone(self.rasaClassifier)

    def test_rasaclassifier_should_classify_claimcategory(self):
        classifier_output = self.rasaClassifier.classify_problem_category("I am being kicked out.")
        self.assertIsNotNone(classifier_output)

    def test_rasaclassifier_should_extract_factentities(self):
        classifier_output = self.rasaClassifier.classify_fact("is_student", "I am a student.")
        self.assertIsNotNone(classifier_output)

    def test_rasaclassifier_shouldnt_extract_nonexistent_factentities(self):
        classifier_output = self.rasaClassifier.classify_fact("does_not_exist", "I am a student.")
        self.assertIsNone(classifier_output)
