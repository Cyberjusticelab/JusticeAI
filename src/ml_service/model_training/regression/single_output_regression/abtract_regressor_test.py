import unittest
from unittest import mock
from model_training.regression.single_output_regression.abstract_regressor import AbstractRegressor
import numpy


class TestRegressionDriver(unittest.TestCase):
    def test_data_metrics(self):
        mock_data = [
            {
                'facts_vector': [1, 2, 3, 4, 5],
                'outcomes_vector': [5, 6]
            },
            {
                'facts_vector': [7, 7, 11, 22, 23],
                'outcomes_vector': [65, 34]
            },
            {
                'facts_vector': [65, 2, 123, 1, 23],
                'outcomes_vector': [4, 76]
            }
        ]
        mock_regressor_name = "example"
        mock_outcome_index = 0
        abstract_regressor = AbstractRegressor(mock_regressor_name, mock_data, mock_outcome_index)
        result = abstract_regressor.data_metrics()
        expected_result = {
            'regressor': {
                'example': {
                    'variance': 813.5555555555555,
                    'std': 28.522895287041873,
                    'mean': 24.666666666666668,
                    'mean_facts_vector': numpy.array([
                        24.33333333,
                        3.66666667,
                        45.66666667,
                        9,
                        17
                    ]
                    )
                }
            }
        }

        self.assertEqual(int(result['regressor']['example']['variance']),
                         int(expected_result['regressor']['example']['variance']))
        self.assertEqual(int(result['regressor']['example']['std']),
                         int(expected_result['regressor']['example']['std']))
        self.assertEqual(int(result['regressor']['example']['mean']),
                         int(expected_result['regressor']['example']['mean']))

        result_vector = result['regressor']['example']['mean_facts_vector']
        expected_vector = expected_result['regressor']['example']['mean_facts_vector']

        for i in range(len(result_vector)):
            self.assertEqual(int(result_vector[i]), int(expected_vector[i]))
