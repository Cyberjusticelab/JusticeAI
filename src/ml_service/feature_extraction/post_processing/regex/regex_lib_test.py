# -*- coding: utf-8 -*-
import unittest
from util.constant import Path
from feature_extraction.post_processing.regex.regex_lib import RegexLib
from util.file import Load


class RegexLibTest(unittest.TestCase):

    def setUp(self):
        self.regex_lib = RegexLib()
        self.fact_cluster_regex_dict = Load().load_binary("cluster_regex_dict.bin")

    def test_fact_regexes(self):
        for regex_name in self.fact_cluster_regex_dict['fact'].keys():
            regexes = self.regex_lib.get_regexes(regex_name)
            test_file_names = self.fact_cluster_regex_dict['fact'][regex_name]
            total_lines_matched = 0
            total_nb_lines_in_file = 0
            file = open(Path.cluster_directory + 'fact/' + test_file_names[0], "r", encoding="utf-8")

            for line in file:
                if line == '\n':
                    break
                total_nb_lines_in_file += 1
            file.seek(0)
            for regex in regexes:
                for line in file:
                    if line == '\n':
                        break
                    line = '[1] ' + line
                    if regex.search(line):
                        total_lines_matched += 1
                file.seek(0)
            file.close()
            self.assertTrue(total_lines_matched > 0 and total_lines_matched / total_nb_lines_in_file > 0.5)
