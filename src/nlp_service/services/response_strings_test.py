import unittest

from services.response_strings import Responses


class TestResponse(unittest.TestCase):
    def setUp(self):
        self.responseInstance = Responses()

    def test_responses_service(self):
        question = Responses.fact_question("apartment_impropre")
        self.assertTrue(question in self.responseInstance.fact_questions["apartment_impropre"])

    def test_responses_service_empty(self):
        question = Responses.fact_question("does_not_exist")
        self.assertTrue(question in self.responseInstance.fact_questions["missing_response"])

    def test_responses_prediction(self):
        question = Responses.prediction_statement("LEASE_TERMINATION", {"orders_resiliation": 1})
        self.assertTrue(question in self.responseInstance.prediction["LEASE_TERMINATION"]["orders_resiliation"][True])

    def test_responses_prediction_false(self):
        question = Responses.prediction_statement("LEASE_TERMINATION", {"orders_resiliation": 0})
        self.assertTrue(question in self.responseInstance.prediction["LEASE_TERMINATION"]["orders_resiliation"][False])

    def test_responses_prediction_empty(self):
        question_bad_category = Responses.prediction_statement("does_not_exist", {})
        question_empty_predictions = Responses.prediction_statement("LEASE_TERMINATION", {})

        self.assertTrue(question_bad_category in self.responseInstance.prediction["missing_category"])
        self.assertTrue(question_empty_predictions in self.responseInstance.prediction["missing_category"])
