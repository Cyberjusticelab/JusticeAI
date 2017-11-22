# -*- coding: utf-8 -*-
import unittest
import re
import os
from global_variables.global_variable import Global
from feature_extraction.regex.regex_facts import TagPrecedents


class RegexTest(unittest.TestCase):

    def test_regex_model(self):
        re_tag = TagPrecedents()
        re_tag.tag_precedents(10)
        binary_model_path = Global.output_directory + r'fact_dict/fact_dict.bin'
        self.assertTrue(os.path.isfile(binary_model_path))

    def test_tag_precedents(self):
        precedent_tagger = TagPrecedents()
        precedent_tagger.precedents_directory_path = Global.test_data_directory + "sample_precedent/"
        precedent_tagger.regexes = {"regex_facts": [("some_fact", [re.compile("fermentum", re.IGNORECASE)])],
                                    "regex_demands": [("some_demand", [re.compile("réclame", re.IGNORECASE)])]}
        facts_found = precedent_tagger.tag_precedents(1)
        self.assertEqual(facts_found["1.txt"]["facts_vector"], [1])
        self.assertEqual(facts_found["2.txt"]["demands_vector"], [0])
