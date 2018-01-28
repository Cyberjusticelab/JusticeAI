import unittest
from feature_extraction.post_processing.regex.regex_entity_extraction import EntityExtraction
import regex as re


class RegexPostLogicTest(unittest.TestCase):
    def test_match_fail(self):
        text = "I am a super saiyan"
        EntityExtraction.regex_bin = {
            'MONEY_REGEX': r"(\d+(\s|,)){1,4}(\s\$|\$)"
        }
        regex_array = [
            re.compile(
                r"\[[123]\]" + r".+" + r"(demand|réclam)(ait|e|ent|aient)" + r" la résiliation du bail",
                re.IGNORECASE
            ),
            re.compile(
                r"\[[123]\]" + r".+une demande en résiliation de bail",
                re.IGNORECASE
            )
        ]
        regex_type = 'BOOLEAN'
        result = EntityExtraction.match_any_regex(text, regex_array, regex_type)
        self.assertFalse(result[0])
        self.assertEqual(result[1], 0)

    def test_match_money(self):
        text = "[3] word locateur 50 $ dommages-intérêts"
        EntityExtraction.regex_bin = {
            'MONEY_REGEX': r"(\d+(\s|,)){1,4}(\s\$|\$)"
        }
        regex_array = [
            re.compile(
                r"\[[123]\]" + r".+" + r"locat(eur|rice)(s)?" +
                r".*" + r"(\d+(\s|,)){1,4}(\s\$|\$)" + r".*dommages-intérêts",
                re.IGNORECASE
            )]
        regex_type = 'MONEY_REGEX'
        result = EntityExtraction.match_any_regex(text, regex_array, regex_type)
        self.assertTrue(result[0])
        self.assertEqual(int(result[1]), 50)

    def test_match_boolean(self):
        text = "[3] une demande en résiliation de bail"
        EntityExtraction.regex_bin = {
            'MONEY_REGEX': r"(\d+(\s|,)){1,4}(\s\$|\$)"
        }
        regex_array = [
            re.compile(
                r"\[[123]\]" + r".+" + r"(demand|réclam)(ait|e|ent|aient)" + r" la résiliation du bail",
                re.IGNORECASE
            ),
            re.compile(
                r"\[[123]\]" + r".+une demande en résiliation de bail",
                re.IGNORECASE
            )
        ]
        regex_type = 'BOOLEAN'
        result = EntityExtraction.match_any_regex(text, regex_array, regex_type)
        self.assertTrue(result[0])
        self.assertEqual(result[1], 1)

    def test_match_date(self):
        text = "[3]l'indemnité additionnelle prévue à l'article 1619 C.c.Q., à compter du 9èr octobre 2014. random text"
        regex_array = [
            re.compile(
                r"l'indemnité additionnelle prévue à l'article 1619 C\.c\.Q\., à compter du \K(?i)\d{1,2}(er|èr|ere|em|eme|ème)? \w{3,9} \d{4}",
                re.IGNORECASE
            )
        ]
        regex_type = 'DATE_REGEX'
        result = EntityExtraction.match_any_regex(text, regex_array, regex_type)
        self.assertTrue(result[0])
        self.assertEqual(result[1], 1412812800.)
