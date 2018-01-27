# -*- coding: utf-8 -*-
import unittest
import codecs
import os
from sys import stdout

import sys

from util.constant import Path
from util.log import Log
from feature_extraction.post_processing.regex import regex_lib


class RegexLibTest():

    def run(self):
        self.regex_cluster_dict = {}
        self.regex_lib = regex_lib.RegexLib()
        self.fact_regexes = self.regex_lib.regex_facts
        self.test_matchRegexesToClusterFiles()

    def test_matchRegexesToClusterFiles(self):

        fact_cluster_directory = Path.cluster_directory + "fact/"
        max_files = 10
        file_parsed = 0
        try:
            if file_parsed > max_files:
                return
            for file in os.listdir(fact_cluster_directory):
                regex_match = self.test_match_file_to_regex(codecs.open(fact_cluster_directory+file, encoding='ISO-8859-1'))
                if regex_match:
                    self.regex_cluster_dict[regex_match] = file
        except FileNotFoundError:
            Log.write("Precedent not found. Please download dataset")
            sys.exit(0)
        print("\ndict:\n")
        for val in self.regex_cluster_dict:
            print(val)

    def test_match_file_to_regex(self,file):
        for fact_regex in self.fact_regexes:
            if self.regex_lib.regex_matches_file(fact_regex[0], file, .1):
                return fact_regex[0]
        return None

RegexLibTest().run()