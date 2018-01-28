# -*- coding: utf-8 -*-
import unittest
from util.constant import Path
from feature_extraction.post_processing.regex.regex_lib import RegexLib
from util.file import Load


class RegexLibTest(unittest.TestCase):

    def setUp(self):
        self.regex_lib = RegexLib()
        self.fact_cluster_regex_dict = Load().load_binary("cluster_regex_dict")
        print("done")

    def test_fact_regexes(self):
        for regex_name in self.fact_cluster_regex_dict.keys():
            regexes = self.regex_lib.get_regexes(regex_name)
            test_file_names = self.fact_cluster_regex_dict[regex_name]
            total_lines_matched = 0
            total_nb_lines_in_file = 0
            for file_name in test_file_names:
                file = open(Path.cluster_directory + 'fact/' + file_name, "r", encoding="utf-8")
                for line in file:
                    total_nb_lines_in_file += 1
                    for regex in regexes:
                        if regex.search(line):
                            total_lines_matched += 1
                file.close()
            self.assertFalse(total_lines_matched > 0 and total_lines_matched / total_nb_lines_in_file > 0.5)
        self.assertTrue(True)