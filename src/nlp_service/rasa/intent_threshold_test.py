import unittest

from rasa.intent_threshold import IntentThreshold


class TestIntentThreshold(unittest.TestCase):
    intentThreshold = None

    @classmethod
    def setUpClass(cls):
        cls.intentThreshold = IntentThreshold(min_percent_difference=0.3, min_confidence_threshold=0.4)

    def test_instantiate(self):
        self.assertIsNotNone(self.intentThreshold)

    def test_is_sufficient(self):
        classify_dict = {
            'intent': {
                'confidence': 0.8
            },
            'intent_ranking': [
                {'confidence': 0.8},
                {'confidence': 0.5}
            ]
        }
        self.assertTrue(self.intentThreshold.is_sufficient(classify_dict))

    def test_is_sufficient_below(self):
        classify_dict = {
            'intent': {
                'confidence': 0.35
            },
            'intent_ranking': [
                {'confidence': 0.35},
                {'confidence': 0.20}
            ]
        }
        self.assertFalse(self.intentThreshold.is_sufficient(classify_dict))

    def test_is_sufficient_single(self):
        classify_dict = {'intent_ranking': [{'confidence': 0.5}]}
        self.assertTrue(self.intentThreshold.is_sufficient(classify_dict))

    def test_percent_difference(self):
        intent_dict = {
            'intent_ranking': [
                {'confidence': 0.5},
                {'confidence': 0.5}
            ]
        }
        self.assertEqual(self.intentThreshold.intent_percent_difference(intent_dict), 0)
