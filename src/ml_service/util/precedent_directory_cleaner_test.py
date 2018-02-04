import unittest
import util.precendent_directory_cleaner as directory_cleaner
from util.constant import Path


class PrecendentDirectoryCleanerTest(unittest.TestCase):
    def test_precendent_removal(self):
        total_files_removed = directory_cleaner.remove_files(Path.test_data_directory)
        self.assertEqual(total_files_removed, ([], []))
