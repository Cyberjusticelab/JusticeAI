import unittest
import main
from util.constant import Path


class TestMain(unittest.TestCase):

    def test_command_line(self):
        raw_data_directory = Path.raw_data_directory
        Path.raw_data_directory = Path.test_mock_precedent_directory

        # preprocessing
        command_list = ["python3", "-pre", "10"]
        self.assertTrue(main.Command.execute(command_list))

        # post processing
        command_list = ["python3", "-post"]
        self.assertTrue(main.Command.execute(command_list))

        # bad command
        command_list = ["python3", "-random"]
        self.assertTrue(not main.Command.execute(command_list))

        Path.raw_data_directory = raw_data_directory
