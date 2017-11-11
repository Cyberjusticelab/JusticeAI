from os import abort

from flask import make_response, jsonify

from controllers.nlpController import __extract_entity, rasaClassifier, , minimum_percent_difference, classify_claim_category, classify_fact_value, classify_fact_value, __classify_claim_category

from services import mlService
from services.responseStrings import Responses
from src.postgresql_db.models import Conversation
from test import conftest


class TestClass(object):


# Sample answer
{'intent': {'name': 'true', 'confidence': 0.96744463217454135}, 'entities': [],
 'intent_ranking': [{'name': 'true', 'confidence': 0.96744463217454135},
                    {'name': 'false', 'confidence': 0.032555367825458557}], 'text': 'I am a student.'}


def test_classify_fact_value():
    assert classify_fact_value(1525125, "I am a student") is not None


def test_classify_claim_category():
    assert __classify_claim_category("I am a student") is not None


def test_extract_entity():
    assert __extract_entity() is not None


def test_is_answer_sufficient():
    assert __extract_entity() is not None
