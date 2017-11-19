import unittest
from feature_extraction.regex.regex_facts import RegexPrecedents
import os
from global_variables.global_variable import Global


class RegexTest(unittest.TestCase):

    # incomplete unittest now. Just a skeleton
    def test_regex_tag(self):
        re_tag = RegexPrecedents()
        re_tag.tag_precedents(10)
        binary_model_path = Global.output_directory + r'fact_matrix_dir/fact_matrix'
        self.assertTrue(os.path.isfile(binary_model_path))