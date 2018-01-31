# -*- coding: utf-8 -*-
import unittest
from util.constant import Path
from feature_extraction.post_processing.regex import regex_lib_helper
from util.file import Load


class RegexLibTest(unittest.TestCase):

    def setUp(self):
        self.fact_cluster_regex_dict = Load().load_binary('cluster_regex_dict.bin')

    def test_fact_demand_regexes(self):
        regex_types = ['fact', 'demand']
        for regex_type in regex_types:
            for regex_name in self.fact_cluster_regex_dict[regex_type].keys():
                regexes = regex_lib_helper.get_regexes(regex_name)
                test_file_names = self.fact_cluster_regex_dict[regex_type][regex_name]
                total_lines_matched = 0
                total_nb_lines_in_file = 0
                file = open(Path.cluster_directory + regex_type + '/' + test_file_names[0], 'r', encoding='utf-8')

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
