import unittest
from model_training.regression.single_output_regression.additional_indemnity import AdditionalIndemnity


class TestAdditionalIndemnity(unittest.TestCase):
    def test_predict(self):
        monthly_rent = 300
        months = 5
        result = int(AdditionalIndemnity().predict(monthly_rent, months))
        expected_result = 89
        self.assertTrue(result == expected_result)
