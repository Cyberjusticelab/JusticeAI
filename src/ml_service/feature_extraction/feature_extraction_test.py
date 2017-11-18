import unittest
from feature_extraction import feature_extraction


class TestStringMethods(unittest.TestCase):

    def test_process_command(self):
        with self.assertRaises(SystemExit) as cm:
            feature_extraction.process_command('random', [])
        self.assertEqual(cm.exception.code, 1)