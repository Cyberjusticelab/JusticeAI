# -*- coding: utf-8 -*-
import re
import unittest
import os

from feature_extraction.post_processing.regex.regex_lib import RegexLib
from feature_extraction.post_processing.regex.regex_test_helper import get_regexes
from util.constant import Path


class RegexLibTest(unittest.TestCase):

    def boolean_test(self, sentences, regex_name):
        # Find the regex corresponding to the test
        generic_regex = get_regexes(regex_name)

        count = 0
        for line in sentences:
            for regex in generic_regex:
                if regex.search(line):
                    count += 1
                    break
        return count == len(sentences)

    def money_test(self, sentences, regex_name, expected_match):
        # Find the regex corresponding to the test
        additional_indemnity_money = get_regexes(regex_name)

        money_matched = []
        for line in sentences:
            for regex in additional_indemnity_money:
                result = regex.search(line)
                if result:
                    money_regex = re.compile(RegexLib.MONEY_REGEX, re.IGNORECASE)
                    money_matched.append(money_regex.search(result.group(0)).group(0))
        return money_matched == expected_match

    def test_regexes(self):
        for file_name in os.listdir(Path.test_regex_directory):
            regex_name = file_name.replace('.txt', '')

            file = open(Path.test_regex_directory + file_name, "r", encoding="utf-8")

            sentences = []
            expected_match = None

            for line in file:
                if line == '\n':
                    continue

                if line.startswith('expected_match ='):
                    match_data = line.replace('expected_match =', '').strip()
                    expected_match = match_data.split(',')
                    continue
                sentences.append(line)
            file.close()

            if expected_match:
                self.assertTrue(self.money_test(sentences, regex_name, expected_match))
            else:
                self.assertTrue(self.boolean_test(sentences, regex_name))

    def test_tenant_not_paid_lease_timespan(self):
        sentences = [
            "La preuve a établi que le loyer réclamé pour les mois de juin, juillet, août et septembre 2014 n'est " +\
            "pas payé et que la somme de 1 620 $ est encore en souffrance.",

            "Les sous-locataires ont quitté le logement concerné au mois de novembre 2014 et les locataires n'ont " +\
            "pas payé au locateur le loyer du mois d'octobre (850 $) et novembre 2014.",

            "qu'ils n'ont pas payé les loyers dus pour les mois de décembre 2014 et janvier 2015 à ce jour " +\
            "non plus",

            "La locataire devrait maintenant cinq (5) mois de loyer",

            "La locataire n'a pas payé ce dernier mois de loyer exigible",

            "La preuve a établi que le loyer réclamé pour le mois de janvier 2013 n'est pas payé et que " +\
            "la somme de 400 $ est encore en souffrance.",

            "la preuve révèle que la locataire n'a pas payé le loyer d'octobre 2012 au montant de 720 $",

            "À ce titre, il soumet que le loyer de décembre 2014 a été payé seulement la veille de l'audience soit " +\
            "le 7 janvier 2015 alors que le loyer de janvier 2015 n'est toujours pas payé.",

            "La locatrice démontre toutefois que le loyer est fréquemment payé en retard, ce qui lui cause un " +\
            "préjudice sérieux dans la gestion de son immeuble. Le bail n'a débuté qu'en juillet 2014. Déjà en " +\
            "août, la locatrice a été contrainte de s'adresser au Tribunal parce que le loyer n'était pas payé. " +\
            "Le bail a été résilié parce que deux mois n'étaient pas payés",

            "il mentionne que la locataire a retenu un montant de 250 $ lors du paiement du loyer du mois de mai et " +\
            "qu'un autre mois n'est pas payé (500 $).",

            "mais qu'elle n'a pas payé les loyers dus pour les mois d'avril et mai 2017 à ce jour non plus, " +\
            "devant ainsi au locateur une somme additionnelle de 1 500 $.",

            "La preuve a établi que le loyer réclamé pour les mois de septembre (344,17 $) et octobre 2014 " +\
            "n'est pas payé"
        ]

        expected_months = [
            ['juin', 'juillet', 'août', 'septembre'],
            ['novembre', "d'octobre", 'novembre'],
            ['décembre', 'janvier'],
            ['janvier'],
            ["d'octobre"],
            ['décembre', 'janvier', 'janvier'],
            ['mai'],
            ['mai', "d'avril", 'mai'],
            ['septembre', 'octobre']
        ]

        # Find the regex corresponding to the test
        regex_list = RegexLib.regex_facts
        tenant_not_paid_lease_timespan = None
        for regex in regex_list:
            if regex[0] == 'tenant_not_paid_lease_timespan':
                tenant_not_paid_lease_timespan = regex[1]

        # perform test
        expected_matches = 9
        match_count = 0
        month_matched = []
        for line in sentences:
            for regex in tenant_not_paid_lease_timespan:
                if regex.search(line):
                    match_count += 1
                    date_regex = re.compile(RegexLib.DATE_REGEX, re.IGNORECASE)
                    month_matched.append(date_regex.findall(line))
        self.assertEqual(match_count, expected_matches)
        self.assertEqual(month_matched, expected_months)
