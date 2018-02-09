import unittest
from model_training.regression import regression_driver


class TestRegressionDriver(unittest.TestCase):
    def test_failure(self):
        command_list = ['random']
        dataset = None
        result = regression_driver.run(command_list, dataset)
        self.assertFalse(result)