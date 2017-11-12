from controllers.nlpController import classify_fact_value, classify_claim_category
import pytest


class TestNlpController(object):
    # Import Private Methods

    dict = {'intent': {'name': 'true', 'confidence': 0.96744463217454135}, 'entities': [],
            'intent_ranking': [{'name': 'true', 'confidence': 0.96744463217454135},
                               {'name': 'false', 'confidence': 0.032555367825458557}], 'text': 'I am a student.'}

    #Testing pytest
    def test_dict(self):
        assert dict is not None

    def test_classify_claim_category(self):
        assert classify_claim_category(1525125, "I am being evicted by my landlord") is not None

    def test_classify_fact_value(self):
        assert classify_fact_value(1525125, "I study at McGill University") is not None

