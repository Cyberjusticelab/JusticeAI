import unittest
import util.precendent_directory_cleaner as directory_cleaner
from util.constant import Path


class PrecendentDirectoryCleanerTest(unittest.TestCase):
    def test_precendent_removal(self):
        total_files_removed = directory_cleaner.remove_files(Path.cluster_directory + 'fact/')
        self.assertEqual(total_files_removed[0].__len__(), 0)
        self.assertEqual(total_files_removed[1].__len__(), 59)
