import unittest
from model_training import training_driver
from util.constant import Path

Path.raw_data_directory = Path.test_data_directory


class TrainingDriverTest(unittest.TestCase):
    def test_feature_extraction(self):

        command_list = ["--svm", "--sf", "10"]
        result = training_driver.run(command_list)
        self.assertTrue(result)

        command_list = ["--svm", "10"]
        result = training_driver.run(command_list)
        self.assertTrue(result)

        command_list = ["--sf", "10"]
        result = training_driver.run(command_list)
        self.assertTrue(result)

        command_list = ['--badarg', "10"]
        result = training_driver.run(command_list)
        self.assertFalse(result)
