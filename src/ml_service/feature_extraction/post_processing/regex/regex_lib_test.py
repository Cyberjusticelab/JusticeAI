# -*- coding: utf-8 -*-
import re
import unittest

from feature_extraction.post_processing.regex.misc import regex_lib_helper
from feature_extraction.post_processing.regex.regex_lib import RegexLib
from util.constant import Path
from util.file import Load


class RegexLibTest(unittest.TestCase):

    def boolean_test(self, sentences, regex_name):
        # Find the regex corresponding to the test
        regex_list = RegexLib.regex_outcomes
        generic_regex = None
        for regex in regex_list:
            if regex[0] == regex_name:
                generic_regex = regex[1]

        count = 0
        for line in sentences:
            for regex in generic_regex:
                if regex.search(line):
                    count += 1
        return count == len(sentences)

    def money_test(self, sentences, regex_name, expected_match):
        # Find the regex corresponding to the test
        regex_list = RegexLib.regex_outcomes
        additional_indemnity_money = None
        for regex in regex_list:
            if regex[0] == regex_name:
                additional_indemnity_money = regex[1]

        money_matched = []
        for line in sentences:
            for regex in additional_indemnity_money:
                result = regex.search(line)
                if result:
                    money_regex = re.compile(RegexLib.MONEY_REGEX, re.IGNORECASE)
                    money_matched.append(money_regex.search(result.group(0)).group(0))
        return money_matched == expected_match

    # ######################################################################
    #
    # OUTCOMES
    #
    # ######################################################################

    def test_tenant_ordered_to_pay_landlord(self):
        sentences = [
            "CONDAMNE la locataire à payer au locateur la somme de 710 $",
            "CONDAMNE les locataires solidairement à payer au locateur la somme de 1 603 $",
            "CONDAMNE le locataire à payer à la locatrice la somme de 4 800 $",
            "CONDAMNE le locataire et la caution solidairement à payer au locateur la somme de 2 497 $"
        ]
        regex_name = 'tenant_ordered_to_pay_landlord'
        expected_match = ['710 $', '1 603 $', '4 800 $', '2 497 $']
        self.assertTrue(self.money_test(sentences, regex_name, expected_match))

    def test_additional_indemnity_money(self):
        sentences = [
            "indemnité additionnelle prévue à l'article 1619 C.c.Q., à compter du 17 octobre 2013 sur la somme " + \
            "de 1 495 $, et sur le solde à ",
            "l'indemnité additionnelle prévue à l'article 1619 C.c.Q., à compter du 7 janvier 2015 sur le montant " + \
            "de 247 $, et"
        ]
        regex_name = 'additional_indemnity_money'
        expected_match = ['1 495 $', '247 $']
        self.assertTrue(self.money_test(sentences, regex_name, expected_match))

    def test_tenant_ordered_to_pay_landlord_legal_fees(self):
        sentences = [
            "CONDAMNE la locataire à payer au locateur la somme de 750 $, plus les frais judiciaires de 72 $",
            "payer au locateur les frais judiciaires de 80 $;",
            "CONDAMNE les locataires à payer au locateur la somme de 1 800 $, le tout avec les intérêts au taux" + \
            " légal et l'indemnité additionnelle prévue à l'article 1619 C.c.Q., à compter du 25 février 2015 sur" + \
            " le montant de 600 $, et, sur le solde, à compter de la date d'échéance de chaque loyer, plus les frais" + \
            " judiciaires et de signification de 81 $"
        ]
        regex_name = "tenant_ordered_to_pay_landlord_legal_fees"
        expected_match = ['72 $', '80 $', '81 $']
        self.assertTrue(self.money_test(sentences, regex_name, expected_match))

    def test_orders_immediate_execution(self):
        sentences = [
            "ORDONNE l'exécution provisoire immédiate de la décision rectifiée, malgré l'appel. ",
            "ORDONNE l'exécution provisoire, malgré l'appel, de l'ordonnance d'expulsion à compter du 11e jour de sa date;"
        ]
        regex_name = 'orders_immediate_execution'
        self.assertTrue(self.boolean_test(sentences, regex_name))

    def test_orders_expulsion(self):
        sentences = [
            "RÉSILIE le bail et ORDONNE l'expulsion des locataires et de tous les occupants du logement;",
            "ORDONNE aux locataires et à tous les occupants du logement de quitter les lieux"
        ]
        regex_name = 'orders_expulsion'
        self.assertTrue(self.boolean_test(sentences, regex_name))

    def test_orders_tenant_pay_first_of_month(self):
        sentences = [
            "ORDONNE au locataire de payer son loyer le 1er de chaque mois, pour la durée du présent bail et du" + \
            "prochain renouvellement;",
            "En cas de paiement avant jugement, ORDONNE à la locataire de payer le loyer le premier jour de chaque terme;",
            "ORDONNE à la locataire de payer ses loyers à échoir le premier jour de chaque mois et ce jusqu'au 31 décembre 2015"
        ]
        regex_name = 'orders_tenant_pay_first_of_month'
        self.assertTrue(self.boolean_test(sentences, regex_name))

    def test_orders_landlord_notify_tenant_when_habitable(self):
        sentences = [
            "ORDONNE au locateur sous toute peine que de droit, d'aviser la locataire dès que le " + \
            "logement sera redevenu propre à l'habitation;"
        ]
        regex_name = 'orders_landlord_notify_tenant_when_habitable'
        self.assertTrue(self.boolean_test(sentences, regex_name))

    def test_authorize_landlord_retake_apartment(self):
        sentences = [
            "AUTORISE le locateur à reprendre le logement à compter du 1er juillet 2015 afin de s'y loger;",
            "AUTORISE le locateur à reprendre possession du logement concerné afin d'y loger",
            "AUTORISE les locateurs à reprendre le logement de la locataire",
            "AUTORISE la locatrice à reprendre possession du logement"
        ]
        regex_name = 'authorize_landlord_retake_apartment'
        self.assertTrue(self.boolean_test(sentences, regex_name))

    # ######################################################################
    #
    # COMPLICATED CASE OF DATES
    #
    # ######################################################################

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


