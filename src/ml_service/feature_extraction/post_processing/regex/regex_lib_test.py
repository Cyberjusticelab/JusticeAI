# -*- coding: utf-8 -*-
import re
import unittest

from feature_extraction.post_processing.regex.misc import regex_lib_helper
from feature_extraction.post_processing.regex.regex_lib import RegexLib
from util.constant import Path
from util.file import Load


class RegexLibTest(unittest.TestCase):
    regex_name_index = 0
    regex_index = 1

    def get_regexes(self, name):
        for fact in RegexLib.regex_facts:
            if fact[self.regex_name_index] == name:
                return fact[self.regex_index]
        for demand in RegexLib.regex_demands:
            if demand[self.regex_name_index] == name:
                return demand[self.regex_index]
        for outcome in RegexLib.regex_outcomes:
            if outcome[self.regex_name_index] == name:
                return outcome[self.regex_index]

        # if name was not found in demands, facts or outcomes
        return None

    def boolean_test(self, sentences, regex_name):
        # Find the regex corresponding to the test
        generic_regex = self.get_regexes(regex_name)

        count = 0
        for line in sentences:
            prev_count =  count
            for regex in generic_regex:
                if regex.search(line):
                    count += 1
            if prev_count == count:
                test = 0
        return count == len(sentences)

    def money_test(self, sentences, regex_name, expected_match):
        # Find the regex corresponding to the test
        additional_indemnity_money = self.get_regexes(regex_name)

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
    # FACTS
    #
    # ######################################################################
    def test_not_violent(self):
        sentences = [
            "Or, pourquoi a-t-il demandé à son neveu d'écrire une lettre, confirmant qu'il n'y a pas eu de "
            "violence s'il est persuadé que l'audition de ce soir ne portera pas sur ce sujet ?",

            "Il précise que le locateur l'a insulté et qu'il n'a jamais utilisé de violence.",

            "Or, pourquoi a-t-il demandé à son neveu d'écrire une lettre, confirmant qu'il n'y a pas eu de "
            "violence s'il est persuadé que l'audition de ce soir ne portera pas sur ce sujet ?",

            "Il prétend cependant que cet avis est invalide puisque la plainte pour agression sexuelle logée au "
            "Service de police n'a pas été retenue. Au surplus, il estime que la locataire a agi ainsi "
            "pour se soustraire à ses obligations et qu'il n'y a aucune preuve de violence.",

            "Bien que l'individu en question n'ait pas été violent ni agressif, elle fut non seulement "
            "surprise par sa présence, mais apeurée et inquiète pour l'avenir, étant une jeune femme vivant seule.",

            "déclare qu'il a de ' bons rapports ' dans l'immeuble depuis 20 ans et que ' ça va très bien ',"
            " ajoutant qu'il n'a pas d'antécédents de violence. Toutefois, la preuve prépondérante démontre "
            "des faits et gestes inquiétants, multiples et sérieux depuis au moins 2012.",

            "Il nie avoir pris la locatrice par le bras; il déclare l'avoir poussé hors du logement par "
            "le bras droit et ajoute que ce geste n'était pas violent.",

            "Cette dernière n'avait pas de marque de violence, n'avait pas de blessures et il n'y "
            "avait pas de dégâts. La locataire n'aurait pas déposé de plainte.",

            "Monsieur T n'a pas fait preuve de violence et ne démontre "
            "pas une propension à adopter ce type de comportement. ",

            "Sûrement, savait-elle que le locataire prendrait mal la nouvelle, ce qui fut le cas,"
            " bien qu'il a été en mesure de se contrôler et de ne pas recourir à la violence."
        ]
        self.assertTrue(self.boolean_test(sentences, 'not_violent'))

    def test_apartment_dirty(self):
        sentences = [
            "a démontré que le problème d'infestation de fourmis était d'une part beaucoup plus important que ce que "
            "le locateur croyait et d'autre part, qu'il ne pouvait résulter d'un mauvais entretien du logement",

            "en ce qui concerne la demande en dommage pour troubles et inconvénients, la preuve est à l'effet "
            "qu'il y avait une infestation de punaises dans le logement du locataire qui somme toute semble avoir "
            "été contrôlé rapidement",

            "cependant, le tribunal estime qu'en raison des inconvénients tout de même importants de la présence de "
            "punaises de lit qui trouble la jouissance paisible des lieux loués, il y a lieu d'accorder à la locataire",

            "la firme d'extermination mentionnent qu'il n'y a qu'une faible infestation de rat de lit à "
            "certains moments, il n'en demeure pas moins que dans les circonstances propres du présent "
            "dossier, c'est-à-dire que ",

            "la locataire est en fait une personne âgée habitant dans une résidence spécifique à un tel groupe de"
            " personnes, le locateur doit s'attendre à ce que les inconvénients de la présence de punaises de lit",

            "puissent être davantage perturbants lorsque vécus par une locataire telle que celle en l'espèce qui,"
            " sans l'ombre d'un doute, a été inquiétée d'une manière importante par l'infestation de ces insectes",

            "cependant, il est anormal de trouver des excréments d'oiseau dans une résidence à la prise de possession "
            "des lieux et, à ce titre, le tribunal estime qu'il est justifié d'accorder aux locataires ",

            "le tribunal estime qu'en raison de l'importance de l'infestation de punaises de lit et qu'au surplus, "
            "plusieurs traitements n'ont donné aucun résultat jusqu'à ce jour, "
            "la locataire justifie l'ordonnance d'exécution ",

            "provisoire de la présente décision afin que son bail soit résilié sur-le-champ et qu'elle cesse de vivre "
            "dans un logement où elle n'a plus aucun meuble ni aucuns biens d'importance, ces derniers "
            "ayant été mis au rebut en raison de la présence de punaises de lit",

            "quant aux dommages réclamés du locataire et à une diminution de loyer, le tribunal doit trancher "
            "le présent litige en disposant des obligations réciproques des parties lorsque le logement concerné "
            "est victime d'une infestation soudaine et imprévue de punaises de lit",

            "le tribunal accorde à la locataire une diminution de loyer globale "
            "de 750 $ pour les cinq mois qu'a duré l'infestation de punaises",

            "la représentante de la locatrice réclame des factures de traitement de "
            "punaises de lit qu'elle a dû débourser, soit plus de 3 000 $ en 2016 pour "
            "des traitements d'un 4 à 5 logements dont celui du locataire",

            "la locataire a produit à la régie du logement une demande de diminution "
            "mensuelle de loyer de 100 $ à compter du 17 mai 2016 et de dommages-intérêts "
            "de 1 500 $ à la suite d'une infestation de fourmis",

            "le locataire prétend qu'une diminution de 250 $ par mois rétablirait "
            "l'équilibre entre son loyer mensuel (515 $) et le fait que le locateur n'a pas "
            "réussi à mettre fin à une infestation de punaises de lit dans son logement",
        ]
        self.assertTrue(self.boolean_test(sentences, 'apartment_dirty'))

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


