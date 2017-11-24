import unittest

from services.responseStrings import Responses


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
        question = Responses.prediction_statement("LEASE_TERMINATION", True)
        self.assertTrue(question in self.responseInstance.prediction["LEASE_TERMINATION"]['success'])

    def test_responses_prediction_fail(self):
        question = Responses.prediction_statement("LEASE_TERMINATION", False)
        self.assertTrue(question in self.responseInstance.prediction["LEASE_TERMINATION"]['fail'])

    def test_responses_prediction_empty(self):
        question = Responses.prediction_statement("does_not_exist", True)
        self.assertTrue(question in self.responseInstance.prediction["missing_category"])
