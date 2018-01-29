import unittest

from services.static_strings import StaticStrings


class StaticStringsTest(unittest.TestCase):
    def test_static_strings(self):
        string = StaticStrings.chooseFrom(StaticStrings.problem_inquiry_landlord)
        self.assertTrue(string in StaticStrings.problem_inquiry_landlord)
