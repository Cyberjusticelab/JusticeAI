import unittest

from rasa.intent_threshold import IntentThreshold
from rasa.rasa_classifier import RasaClassifier


class TestNLPIntegration(unittest.TestCase):
    rasaClassifier = None
    intentThreshold = None

    @classmethod
    def setUpClass(cls):
        cls.rasaClassifier = RasaClassifier()
        cls.rasaClassifier.train(force_train=True)
        cls.intentThreshold = IntentThreshold(min_percent_difference=0.3, min_confidence_threshold=0.4)

    def test_claim_category_lease_termination(self):
        sentences = [
            "I'm being kicked out of my house.",
            "I'm being evicted from my apartment",
            "I'm kicking out my tenant.",
            "I want to break my lease"
        ]

        for sentence in sentences:
            classify_dict = self.rasaClassifier.classify_problem_category(sentence)
            determined_claim_category = classify_dict['intent']['name']
            self.assertTrue(self.intentThreshold.is_sufficient(classify_dict))
            self.assertTrue(determined_claim_category == "ask_lease_termination")
