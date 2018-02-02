# -*- coding: utf-8 -*-
import unittest
import re
import os
from util.constant import Path
from feature_extraction.post_processing.regex.regex_tagger import TagPrecedents


class RegexTaggerTest(unittest.TestCase):
    def setUp(self):
        self.precedent_tagger = TagPrecedents()
        self.precedent_tagger.regexes = {"regex_facts": [("some_fact", [re.compile("fermentum", re.IGNORECASE)], 'BOOLEAN')],
                                         "regex_demands": [("some_demand", [re.compile("réclame", re.IGNORECASE)], 'BOOLEAN')],
                                         "regex_outcomes": [("some_outcome", [re.compile("REJETTE")], 'BOOLEAN')]
                                         }

    def test_regex_model(self):
        binary_directory = Path.binary_directory
        Path.binary_directory = Path.test_data_directory
        self.precedent_tagger.precedents_directory_path = Path.test_data_directory

        self.precedent_tagger.tag_precedents(10)
        binary_model_path = Path.binary_directory + r'precedent_vectors.bin'
        self.assertTrue(os.path.isfile(binary_model_path))

        os.remove(binary_model_path)
        Path.binary_directory = binary_directory

    def test_tag_precedents(self):
        binary_directory = Path.binary_directory
        self.precedent_tagger.precedents_directory_path = Path.test_data_directory
        Path.binary_directory = Path.test_data_directory

        facts_found = self.precedent_tagger.tag_precedents(2)

        self.assertEqual(facts_found["1.txt"]["facts_vector"], [1])
        self.assertEqual(facts_found["2.txt"]["demands_vector"], [0])

        binary_model_path = Path.binary_directory + r'precedent_vectors.bin'
        os.remove(binary_model_path)
        Path.binary_directory = binary_directory

    def test_intent_indice(self):
        binary_directory = Path.binary_directory
        Path.binary_directory = Path.test_data_directory

        regex_list = self.precedent_tagger.get_intent_index()
        self.assertEqual(regex_list["facts_vector"][0], (0, "some_fact", 'bool'))
        self.assertEqual(regex_list["demands_vector"][0], (0, "some_demand", 'bool'))

        Path.binary_directory = binary_directory
