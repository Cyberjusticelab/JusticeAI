# -*- coding: utf-8 -*-
import unittest

from feature_extraction.post_processing.regex.misc import regex_lib_helper


class RegexLibHelperTest(unittest.TestCase):

    def test_regex_finder(self):
        sentence = '[1] considérant que la preuve démontre que le locataire paie souvent son loyer en retard, causant ainsi au locateur un préjudice sérieux;'
        self.assertTrue('tenant_continuous_late_payment' in regex_lib_helper.regex_finder(sentence))

    def test_get_regexes(self):
        regex_lib_helper.get_regexes('additional_indemnity_money')
        self.assertIsNone(None)
