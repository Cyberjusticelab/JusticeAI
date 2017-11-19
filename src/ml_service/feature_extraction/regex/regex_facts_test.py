# -*- coding: utf-8 -*-
import unittest
from feature_extraction.regex.regex_facts import RegexPrecedents
from feature_extraction.regex.regex_lib import RegexLib
import os
from global_variables.global_variable import Global


class RegexTest(unittest.TestCase):

    # incomplete unittest now. Just a skeleton
    def test_regex_model(self):
        pass
        '''
        re_tag = RegexPrecedents()
        re_tag.tag_precedents(10)
        binary_model_path = Global.output_directory + r'fact_matrix_dir/fact_matrix'
        self.assertTrue(os.path.isfile(binary_model_path))
        '''

    def test_regex_demands(self):
        directory = Global.regex_data_directory + 'demands'
        for filename in os.listdir(directory):
            intent = filename.split('-')[1]
            intent = intent.replace('.txt', '')
            for regex in RegexLib.regex_demands:
                if regex[0] == intent:
                    file = Global.regex_data_directory + 'demands/' +filename
                    self.assertTrue(self.regex_file(file, regex[1]))


    def test_regex_facts(self):
        directory = Global.regex_data_directory + 'facts'
        for filename in os.listdir(directory):
            intent = filename.split('-')[1]
            intent = intent.replace('.txt', '')
            for regex in RegexLib.regex_demands:
                if regex[0] == intent:
                    file = Global.regex_data_directory + 'facts/' +filename
                    self.assertTrue(self.regex_file(file, regex[1]))

    def regex_file(self, filename, regex):
        file = open(filename, 'r', encoding="utf-8")
        for line in file:
            if not regex.match(line):
                file.close()
                print(regex)
                print(line)
                print(file)
                return False
        file.close()
        return True