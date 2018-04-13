import unittest
from feature_extraction import feature_extraction_driver
from util.constant import Path


class TestFeatureExtraction(unittest.TestCase):
    def test_feature_extraction(self):
        raw_data_directory = Path.raw_data_directory
        Path.raw_data_directory = Path.test_mock_precedent_directory

        # preprocessing
        command_list = ["-pre", "10"]
        self.assertTrue(feature_extraction_driver.run(command_list))

        # post processing
        command_list = ["-post", "10"]
        self.assertTrue(feature_extraction_driver.run(command_list))

        # bad command
        command_list = ["python3", "-random"]
        self.assertTrue(not feature_extraction_driver.run(command_list))

        Path.raw_data_directory = raw_data_directory
