import os
import unittest

from rasa.rasa_classifier import RasaClassifier

from postgresql_db.models import PersonType


class TestRasaClassifier(unittest.TestCase):
    rasaClassifier = None

    @classmethod
    def setUpClass(cls):
        cls.rasaClassifier = RasaClassifier()
        cls.rasaClassifier.train(force_train=False)

    def test_instantiate(self):
        self.assertIsNotNone(self.rasaClassifier)

    def test_classify_claimcategory(self):
        classifier_output = self.rasaClassifier.classify_problem_category("I am being kicked out.", PersonType.TENANT.value)
        self.assertIsNotNone(classifier_output)

    def test_extract_factentities(self):
        classifier_output = self.rasaClassifier.classify_fact("apartment_impropre", "No")
        self.assertIsNotNone(classifier_output)

    def test_nonexistent_factentities(self):
        classifier_output = self.rasaClassifier.classify_fact("does_not_exist", "Whatever.")
        self.assertIsNone(classifier_output)
