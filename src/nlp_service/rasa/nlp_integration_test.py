import unittest

from rasa.intent_threshold import IntentThreshold
from rasa.rasa_classifier import RasaClassifier
import json
import codecs
import os


class TestNLPIntegration(unittest.TestCase):
    rasaClassifier = None
    intentThreshold = None

    @classmethod
    def setUpClass(cls):
        cls.rasaClassifier = RasaClassifier()
        cls.rasaClassifier.train(force_train=True)
        cls.intentThreshold = IntentThreshold(min_percent_difference=0, min_confidence_threshold=0.25)

    def test_all_claim_category_text(self):
        filepath = os.getcwd() + '/rasa/data/category/claim_category.json'
        data = json.loads(codecs.open(filepath, 'r', 'utf-8').read().encode('utf-8'))
        example_objects = data['rasa_nlu_data']['common_examples']

        for example in example_objects:
            classify_dict = self.rasaClassifier.classify_problem_category(example['text'])
            determined_claim_category = classify_dict['intent']['name']
            self.assertTrue(self.intentThreshold.is_sufficient(classify_dict),
                            "Insufficient Confidence - Intent: {}, Confidence {}"
                            .format(
                                determined_claim_category,
                                classify_dict['intent']['confidence'])
                            )
            self.assertTrue(determined_claim_category == example['intent'],
                            "Wrong Intent Classification\nClassified Intent: {}\nActual Intent: {}\nExample Sentence: {}".format(determined_claim_category, example['intent'], example['text'])
                            )
