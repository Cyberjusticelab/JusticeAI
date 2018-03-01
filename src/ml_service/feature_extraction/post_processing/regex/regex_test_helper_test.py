# -*- coding: utf-8 -*-
import unittest
from feature_extraction.post_processing.regex import regex_test_helper


class RegexLibHelperTest(unittest.TestCase):

    def test_regex_finder(self):
        sentence = '[1] considérant que la preuve démontre que le locataire paie souvent son loyer en retard, causant ainsi au locateur un préjudice sérieux;'
        self.assertTrue('tenant_continuous_late_payment' in regex_test_helper.regex_finder(sentence))

    def test_get_regexes(self):
        self.assertIsNotNone(regex_test_helper.get_regexes('demand_lease_modification'))
