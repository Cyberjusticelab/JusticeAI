import unittest
from feature_extraction import main


class TestStringMethods(unittest.TestCase):

    def test_process_command(self):
        with self.assertRaises(SystemExit) as cm:
            main.process_command('random', [])
        self.assertEqual(cm.exception.code, 1)

    def test_parse_precedence(self):
        with self.assertRaises(SystemExit) as cm:
            main.parse_precedence('random')
        self.assertEqual(cm.exception.code, 1)
