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
        EntityExtraction.regex_bin = {
            'DATE_REGEX': r"(janvier|février|mars|avril|d'avril|mai|juin|juillet|d'août|août|septembre|d'octobre|" +
                          r"octobre|novembre|décembre)"
        }
        text = "[3] l'indemnité additionnelle prévue à l'article 1619 C.c.Q., à compter du 9 octobre 2014"
        regex_array = [
            re.compile(
                r"(l'|)indemnité additionnelle prévue à l'article 1619 C\.c\.Q\., à compter du \d{0,2}" +
                r"(er|èr|ere|em|eme|ème)? (janvier|février|mars|avril|d'avril|mai|juin|" +
                r"juillet|d'août|août|septembre|d'octobre|octobre|novembre|décembre) \d{0,4}",
                re.IGNORECASE
            )
        ]
        regex_type = 'DATE_REGEX'
        result = EntityExtraction.match_any_regex(text, regex_array, regex_type)
        self.assertFalse(result[0])
        self.assertEqual(result[1], 0)

    def test_get_fact_duration(self):
        self.assertEqual(EntityExtraction.get_fact_duration(" pas paye juin, juillet, aout et septembre 2014 ")[1], 4)
        self.assertEqual(EntityExtraction.get_fact_duration(" novembre 2010 et avril 2011 pas paye ")[1], 2)
        self.assertEqual(EntityExtraction.get_fact_duration(" d'avril et mai 2012 pas paye ")[1], 2)
        self.assertEqual(EntityExtraction.get_fact_duration(" pas paye janvier (solde) et fevrier 2011 ")[1], 2)
        self.assertEqual(EntityExtraction.get_fact_duration(" pas paye d'octobre 2014 au mois de mars 2015 ")[1], 6)
        self.assertEqual(EntityExtraction.get_fact_duration(" d'octobre et novembre 2012 (325 $), fevrier (375 $), "
                                                            "mars et avril 2013 pas paye ")[1], 5)
        self.assertEqual(EntityExtraction.get_fact_duration(" loyer des mois d'avril et mai 2014 pas paye ")[1], 2)
        self.assertEqual(
            EntityExtraction.get_fact_duration(" decembre 2013 (350 $), janvier, fevrier et mars 2014 pas paye ")[1], 4)
        self.assertEqual(EntityExtraction.get_fact_duration(" juin 2013 n'est pas paye ")[1], 1)

        self.assertFalse(EntityExtraction.get_fact_duration(" juin 2013 a juin 2015 ")[0])
        self.assertFalse(EntityExtraction.get_fact_duration(
            "fevrier a mai 2017 pour lequel elle a ete condamnee dans la decision contestee ")[0])
