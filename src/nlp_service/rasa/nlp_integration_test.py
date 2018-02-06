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
        cls.rasaClassifier.train(force_train=False)
        cls.intentThreshold = IntentThreshold(min_percent_difference=0, min_confidence_threshold=0.15)

    def test_all_tenant_claim_category(self):
        filepath = os.getcwd() + '/rasa/data/category/category_tenant.json'
        data = json.loads(codecs.open(filepath, 'r', 'utf-8').read().encode('utf-8'))
        common_examples = data['rasa_nlu_data']['common_examples']

        self.test_claim_category_classification(common_examples, "tenant")

    def test_all_landlord_claim_category(self):
        filepath = os.getcwd() + '/rasa/data/category/category_landlord.json'
        data = json.loads(codecs.open(filepath, 'r', 'utf-8').read().encode('utf-8'))
        common_examples = data['rasa_nlu_data']['common_examples']

        self.test_claim_category_classification(common_examples, "landlord")

    def test_claim_category_classification(self, common_examples, person_type):
        for example in common_examples:
            classify_dict = self.rasaClassifier.classify_problem_category(example['text'], person_type)
            determined_claim_category = classify_dict['intent']['name']
            self.assertTrue(self.intentThreshold.is_sufficient(classify_dict),
                            "Insufficient Confidence - Intent: {}\nConfidence {}\nExample Sentence: {}"
                            .format(
                                determined_claim_category,
                                classify_dict['intent']['confidence'],
                                example['text'])
                            )
            self.assertTrue(determined_claim_category == example['intent'],
                            "Wrong Intent Classification\nClassified Intent: {}\nActual Intent: {}\nExample Sentence: {}".format(
                                determined_claim_category, example['intent'], example['text'])
                            )
