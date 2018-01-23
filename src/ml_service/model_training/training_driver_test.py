import unittest
from model_training import training_driver
from util.constant import Path
import os


class TestTrainingDriver(unittest.TestCase):
    def test_command_not_recognized(self):
        command_list = ['--random']
        result = training_driver.run(command_list)
        self.assertFalse(result)

    def test_vector_model_not_found(self):
        # setup
        binary_path = Path.binary_directory
        Path.binary_directory = ""

        # test
        command_list = ['--svm']
        result = training_driver.run(command_list)
        self.assertFalse(result)
        Path.binary_directory = binary_path
