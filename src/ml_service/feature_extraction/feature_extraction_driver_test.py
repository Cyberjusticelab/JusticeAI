import unittest
from feature_extraction import feature_extraction_driver
from util.constant import Path


class TestFeatureExtraction(unittest.TestCase):
    def test_feature_extraction(self):

        raw_data_directory = Path.raw_data_directory
        Path.raw_data_directory = Path.test_data_directory

        # preprocessing
        command_list = ["-pre", "10"]
        self.assertTrue(feature_extraction_driver.run(command_list))

        # clustering
        command_list = ["-cluster", "--kmeans", "--fact", "1"]
        self.assertTrue(feature_extraction_driver.run(command_list))
        command_list = ["-cluster", "--kmeans", "--decision", "1"]
        self.assertTrue(feature_extraction_driver.run(command_list))

        # post processing
        command_list = ["-post", "10"]
        self.assertTrue(feature_extraction_driver.run(command_list))

        # bad command
        command_list = ["python3", "-random"]
        self.assertTrue(not feature_extraction_driver.run(command_list))

        Path.raw_data_directory = raw_data_directory
