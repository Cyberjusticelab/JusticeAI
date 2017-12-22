import unittest
import util.precendent_directory_cleaner as directory_cleaner
from util.constant import Path


class PrecendentDirectoryCleanerTest(unittest.TestCase):

    def test_english_precendent_removal(self):
        total_files_removed = directory_cleaner.remove_language_type_from_directory(Path.test_data_directory, "en")
        self.assertEqual(total_files_removed, 0)
