import unittest
import main
from util.constant import Path


class TestMain(unittest.TestCase):

    def test_command_line(self):
        raw_data_directory = Path.raw_data_directory
        Path.raw_data_directory = Path.test_data_directory

        # preprocessing
        command_list = ["python3", "-pre", "10"]
        self.assertTrue(main.Command.execute(command_list))

        # clustering
        command_list = ["python3", "-cluster", "--kmeans", "--fact", "1"]
        self.assertTrue(main.Command.execute(command_list))
        command_list = ["python3", "-cluster", "--kmeans", "--decision", "1"]
        self.assertTrue(main.Command.execute(command_list))

        # post processing
        command_list = ["python3", "-post"]
        self.assertTrue(main.Command.execute(command_list))

        """
        cannot test this
        # train model
        command_list = ["python3", "-train"]
        main.Command.execute(command_list)
        self.assertTrue(os.path.isfile(Path.binary_directory + "svm_model.bin"))
        """

        # bad command
        command_list = ["python3", "-random"]
        self.assertTrue(not main.Command.execute(command_list))

        Path.raw_data_directory = raw_data_directory
