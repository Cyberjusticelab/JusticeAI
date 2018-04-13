# -*- coding: utf-8 -*-
import regex as re


class RegexLib:
    MONEY_REGEX = r"(\d+(\s|,)){1,4}(\s\$|\$)"
    TENANT_REGEX = r"(partie-)?locataire(s)?"
    LANDLORD_REGEX = r"(partie-)?locat(eur|rice)(s)?"
    DEMAND_REGEX = r"(demand|réclam)(ait|e|ent|aient)"
    DATE_REGEX = r"(?:en\s|de\s|d')?(janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre" \
                 r"|novembre|décembre|decembre)"
    DATE_RANGE_REGEX = r"(?i)(\d{1,2})?(?:er|èr|ere|em|eme|ème)?\s?(\w{3,9}) (\d{4})?\s?" \
                       r"(?:a|à|au|et se terminant le|au mois de) (\d{1,2})?(?:er|èr|ere|em|eme|ème)?\s?(\w{3,9}) (\d{4})"

    def __multiple_words(min, max):
        return r"([a-zA-ZÀ-ÿ0-9]+(\s|'|,\s)){" + str(min) + "," + str(max) + "}"

    # #############################################################
    # FACTS
    # #############################################################

    regex_facts = [
        ("apartment_dirty", [
            re.compile(
                r".+(logement(était\s)?(.+impropre|infesté).+l'habitation|(bon\sétat.+propreté))",
                re.IGNORECASE
            ),
            re.compile(
                r".+menace " +
                __multiple_words(0, 6) + r"(sécurité des occupants|l'intégrité du logement)",
                re.IGNORECASE
            ),
            re.compile(
                r".+preuve.*logement.*" +
                TENANT_REGEX + r".*est.*mauvais.*état",
                re.IGNORECASE
            ),
            re.compile(
                r".+((infestation(s)?|traitement)\s(soudaine et imprévue )?de " + __multiple_words(0, 1) +
                "(insecte(s)?|punaise(s)?|rat(s)?|fourmi(s)?|coquerelle(s)?|souri(s))|excrément(s)?)",
                re.IGNORECASE
            ),
            re.compile(
                r".+présence de punaise(s)? de lit",
                re.IGNORECASE
            ),
            re.compile(
                r".+(" + TENANT_REGEX + r".+)?(apartment.+)?insalubre",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("asker_is_landlord", [
            re.compile(
                r".+ " + __multiple_words(0, 2) + LANDLORD_REGEX + r" " + DEMAND_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("asker_is_tenant", [
            re.compile(
                r".+ " + __multiple_words(0, 2) + TENANT_REGEX + r" " + DEMAND_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("bothers_others", [
            re.compile(
                r".+" + TENANT_REGEX +
                r" trouble(nt|) la jouissance normale des lieux loués",
                re.IGNORECASE
            ),
            re.compile(
                r".+dérange la jouissance paisible",
                re.IGNORECASE
            ),
            re.compile(
                r".+dérange la jouissance",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + TENANT_REGEX +
                r" trouble(nt|) la jouissance",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("disrespect_previous_judgement", [
            re.compile(
                r".+non-respect d'une ordonnance émise antérieurement",
                re.IGNORECASE
            ),
            re.compile(
                r".+pas respecté l'ordonnance de payer " +
                __multiple_words(0, 4) + r"loyer",
                re.IGNORECASE
            ),
            re.compile(
                r".+non-respect de l'ordonnance de payer le loyer",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + TENANT_REGEX + r" " +
                __multiple_words(0, 3) + r"pas respecté l'ordonnance",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_inspector_fees", [
            re.compile(
                r".*\K" + MONEY_REGEX + r"\s(((pour|représentant)\s(les\s|des\s)?)|en\s)?\(?frais\sde\sdépistage\)?",
                re.IGNORECASE
            ),
            re.compile(
                r".*frais\sde\sdépistage\s((au montant\s)?de\s)?" +
                r"\(?\K" + MONEY_REGEX + r"\)?",
                re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("landlord_notifies_tenant_retake_apartment", [
            re.compile(
                r".+" + LANDLORD_REGEX + r".+" +
                TENANT_REGEX + r".+(reprendre|reprise).+logement",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_pays_indemnity", [
            re.compile(
                r".+dédommage.+" + TENANT_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_relocation_indemnity_fees", [
            re.compile(
                r".+(" + LANDLORD_REGEX + r")?.+réclame.+indemnité de relocation\s" + __multiple_words(0, 5)
                + MONEY_REGEX, re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("landlord_rent_change", [
            re.compile(
                r".+l'ajustement.+loyer",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_rent_change_doc_renseignements", [
            re.compile(
                r".+formulaire\s(r|R)enseignements.+loyer",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_retakes_apartment", [
            re.compile(
                r".+" + LANDLORD_REGEX +
                r".+(reprendre|reprise)(.+logement)?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_sends_demand_regie_logement", [
            re.compile(
                r".+" + LANDLORD_REGEX +
                r".+demande.+ordonnance.+(Régie\sdu\slogement)",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + LANDLORD_REGEX +
                r".+(produit|introduit|déposé|intention de faire|déposent).+demand(e|ent).+(Régie\sdu\slogement)",
                re.IGNORECASE
            ),
            re.compile(
                LANDLORD_REGEX + r" demande à la Régie du logement",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_sends_demand_regie_logement", [
            re.compile(
                TENANT_REGEX + r".+ " + __multiple_words(0, 2) + LANDLORD_REGEX +
                r" une mise en demeure.+(demanderait|demande).+Régie du logement",
                re.IGNORECASE
            ),
            re.compile(
                TENANT_REGEX + r" envoie une mise en demeure " + __multiple_words(0, 2) + LANDLORD_REGEX +
                r".+ (demanderait|demande) .+ Régie du logement",
                re.IGNORECASE
            ),
            re.compile(
                TENANT_REGEX + r" demande à la Régie du logement",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("signed_proof_of_rent_debt", [
            re.compile(
                r".+une reconnaissance de dette",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("rent_increased", [
            re.compile(
                r"preuve démontre la réception de l'avis d'augmentation",
                re.IGNORECASE
            ),
            re.compile(
                r"augmentation (du|de) loyer",
                re.IGNORECASE
            ),
            re.compile(
                r"augmentation de " + MONEY_REGEX,
                re.IGNORECASE
            ),
        ], "BOOLEAN"),
        ("tenant_continuous_late_payment", [
            re.compile(
                r".+(fréquen(ce|ts)).*(retard(s)?)?.*(article\s1971)?",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + TENANT_REGEX +
                r" paie(nt|) (\w+\s){0,4}loyer(s|) (\w+\s){0,4}en retard",
                re.IGNORECASE
            ),
            re.compile(
                r".+preuve de retards fréquents dans le paiement du loyer",
                re.IGNORECASE
            ),
            re.compile(
                r".+considérant la preuve des retards fréquents",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_damaged_rental", [
            re.compile(
                r".+" + TENANT_REGEX +
                r" (a|ont) causé des dommages",
                re.IGNORECASE
            ),
            re.compile(
                r"dommage(s|) mat(é|e)riel(s|)",
                re.IGNORECASE
            ),
            re.compile(
                r"dédommagement",
                re.IGNORECASE
            ),
            re.compile(
                r"pertes matérielles",
                re.IGNORECASE
            ),
            re.compile(
                r"dommages-intérêts matériels",
                re.IGNORECASE
            ),
            re.compile(
                r"dommages-matériels",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_dead", [
            re.compile(
                r".+" + TENANT_REGEX +
                r" (est|sont) décédé(e|s|es)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_financial_problem", [
            re.compile(
                r".+(" + TENANT_REGEX +
                r".+)?difficultés.+financières(.+" + TENANT_REGEX + r")?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_group_responsability", [
            re.compile(
                r".+bail.+(prévoit\spas).+" + TENANT_REGEX +
                r".+(solidairement\sresponsables).+" + LANDLORD_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_individual_responsability", [
            re.compile(
                r".+bail.+(prévoit).+" + TENANT_REGEX +
                r".+(solidairement\sresponsables).+" + LANDLORD_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_is_bothered", [
            re.compile( \
 \
                r".+ " + __multiple_words(0, 2) + TENANT_REGEX +
                r" (a|ont) subi(ent|) une perte de jouissance",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_lease_indeterminate", [
            re.compile(
                r".+bail.+durée\sindéterminée",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_left_without_paying", [
            re.compile(
                r".+suite au déguerpissement " + __multiple_words(0, 2) +
                TENANT_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + TENANT_REGEX + r" " +
                __multiple_words(0, 6) +
                r"(a|ont|aurait|auraient) quitté le logement",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + TENANT_REGEX +
                r" (a|ont|aurait|auraient) quitté les lieux loué",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + TENANT_REGEX +
                r" (a|ont) déguerpi (du logement|des lieux loué)",
                re.IGNORECASE
            ),
            re.compile(
                r".+l'article 1975",
                re.IGNORECASE
            ),
            re.compile(
                r".+suite du (départ|déguerpissement) " + __multiple_words(0, 2) +
                TENANT_REGEX,
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_monthly_payment", [
            re.compile(
                r".+loyer\smensuel.*" + MONEY_REGEX,
                re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("tenant_owes_rent", [
            # FIXME or SPLIT
            # re.compile(
            #     r".+(.*preuve.+" + LANDLORD_REGEX + r".+non-paiement.+loyer)?.*(" + TENANT_REGEX + r".+(doi(vent|t))((.+somme\sde)|(total))?.+([\d\s,]+)(\$|\s\$)|" + LANDLORD_REGEX + r".+créance.+" + MONEY_REGEX + r".+loyers\simpayés)|(.*paiement.*arriérés.+loyer.+\b(\d{1,3}(\s\d{3}|,\d{2})*))",
            #     re.IGNORECASE
            # ),
            re.compile(
                r".+" + TENANT_REGEX + \
                r" doi(ven|)t " + __multiple_words(0, 6) + r"" + MONEY_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                r".+" + LANDLORD_REGEX + r" réclame(nt|) " + __multiple_words(
                    0, 6) + r"" + MONEY_REGEX + r"(, soit le loyer| à titre de loyer)",
                re.IGNORECASE
            ),
            re.compile(
                r".+(il|elle)(s|) doi(ven)t toujours une somme de " + MONEY_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                r".+admet devoir la somme de " + \
                MONEY_REGEX + r" à titre de loyer",
                re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("tenant_refuses_retake_apartment", [
            re.compile(
                r".+" + TENANT_REGEX + \
                r".+refus(e|ait|aient).+quitter",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_rent_not_paid_more_3_weeks", [
            re.compile(
                r".+" + TENANT_REGEX + \
                r".+retard.+plus.+((trois semaines)|(trois \(3\) semaines)).+(paiement\sdu\sloyer)",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + TENANT_REGEX + \
                r" (est|sont) en retard " + \
                __multiple_words(1, 8) + r"(trois|3) semaines",
                re.IGNORECASE
            )

        ], "BOOLEAN"),
        ("tenant_withold_rent_without_permission", [
            re.compile(
                r".+" + TENANT_REGEX + \
                r".+ne peut.+faire justice.+retenir.+loyer.+(sans.+Tribunal)?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("violent", [
            # TODO this is too vague, need to redo this
            # re.compile(
            #     r".+violentée|violent(e)?|menaçant(e)?",
            #     re.IGNORECASE
            # ),
            re.compile(
                r".+((c|l)es cris(e|es)?|les hurlements|le tapage|les claquages de portes|les chicanes)",
                re.IGNORECASE
            ),
            re.compile(
                r".+\s(subissait de la|victime(s)? de|sa|propos|(raison\s)?de la|comportement(s)?"
                r"|montre|us(é|er) de|vivre dans la|langage|empreint(s)? de|parfois|est|très|en"
                r"|échange(s)?|cause de|attitude|geste de|si|climat de|acte(s)? de|être|été"
                r"|escalade de|reliées à|altercation(s)?(\sphysique(s)?)|étaient|avec|devenu"
                r"|très|bâton|et|aurait|assez|façon|plus|bruit(s)?|manifestation(s)? (de)?"
                r"|particulièrement|est un (homme|femme)|parole(s)?|coup(s)?|attitude) "
                r"(violen(ce|t(e|é)?)(s)?|(l')?agressi(f|ve|vité)|mena(ce(s)?|çant(s)?)|vulgaire"
                r"|intimida(tion|nt)(s)?|hostile|inadéquat)",
                re.IGNORECASE
            ),
            re.compile(
                r".+((violen(ce|t(e|é)?))(s)?|agressi(f|ve)|mena(ç|c)(e|ant)(s)?) "
                r"(bagarre(s)?|altercation|verbale(s)?|conjugale(s)?|continue|physique(s|ment)?)",
                re.IGNORECASE
            ),
            re.compile(
                r".+(,\s(violen(ce|t(e|é)?)(s)?|(l')?agressi(f|ve|vité)|mena(ce(s)?|çant(s)?)"
                r"|vulgaire|intimida(tion|nt)(s)?|hostile|inadéquat),)+",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_not_paid_lease_timespan", [
            re.compile(
                DATE_REGEX + r" .+n'(est|été|ete|était|etait) pas payé",
                re.IGNORECASE
            ),
            re.compile(
                TENANT_REGEX + r" n'(ont|a|avait) pas payé.+" + DATE_REGEX + r".+et" + DATE_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                TENANT_REGEX + r" n'(ont|a|avait) pas payé le loyer " + DATE_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                "le loyer " + DATE_REGEX + " \d{0,4} n'(est|été|ete|était|etait) toujours pas payé",
                re.IGNORECASE
            ),
            re.compile(
                "pas payé le(s|) loyer(s|) du(s|) pour le(s|) mois " + DATE_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                r"pas payé(s|) " + __multiple_words(0, 2) + LANDLORD_REGEX + r" le(s|) loyer(s|) (du|des) mois "
                + DATE_REGEX, re.IGNORECASE
            )
        ], 'DATE_REGEX')
    ]

    # #############################################################
    # OUTCOMES
    # #############################################################

    regex_outcomes = [
        ("additional_indemnity_money", [
            re.compile(
                r"(l'|)indemnité additionnelle prévue à l'article 1619 C\.c\.Q\., à compter du \d{0,2}(er|èr|" +
                r"ere|em|eme|ème)? " + DATE_REGEX + " \d{0,4} sur (la somme|le montant) de " + MONEY_REGEX,
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("declares_resiliation_is_correct", [
            re.compile(
                r"CONSTATE la résiliation du bail",
                re.IGNORECASE
            ),
            re.compile(
                r"DÉCLARE le bail résilié"
            )
        ], "BOOLEAN"),
        ("landlord_serious_prejudice", [
            re.compile(
                r"préjudice sérieux " + __multiple_words(0, 2) + LANDLORD_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                r"préjudice sérieux " + __multiple_words(0, 2) + LANDLORD_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                LANDLORD_REGEX + r" " +
                __multiple_words(0, 1) + r"}un préjudice sérieux",
                re.IGNORECASE
            ),
            re.compile(
                LANDLORD_REGEX + r" ayant démontré le préjudice sérieux",
                re.IGNORECASE
            ),
            re.compile(
                "préjudice sérieux.+retards",
                re.IGNORECASE
            ),
            re.compile(
                "préjudice sérieux.+gestion.+immeuble",
                re.IGNORECASE
            ),
            re.compile(
                "caus(e|ent) " + __multiple_words(0, 2) + LANDLORD_REGEX + r" un préjudice sérieux",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("orders_expulsion", [
            re.compile(
                r"ORDONNE l'expulsion"
            ),
            re.compile(
                r"ORDONNE " + __multiple_words(0, 2) + TENANT_REGEX + " et à tous les occupants du "
                                                                      "logement de quitter les lieux", re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("orders_immediate_execution", [
            re.compile(
                r"ORDONNE l'exécution provisoire.+malgré l'appel",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("orders_resiliation", [
            re.compile(
                r"RÉSILIE le bail"
            )
        ], "BOOLEAN"),
        ("orders_tenant_pay_first_of_month", [
            re.compile(
                r"ORDONNE " + __multiple_words(0, 2) + TENANT_REGEX + " de payer le loyer le premier jour",
                re.IGNORECASE
            ),
            re.compile(
                r"ORDONNE " + __multiple_words(0, 2) + TENANT_REGEX + " de payer ses loyers à échoir "
                                                                      "le premier jour de chaque mois", re.IGNORECASE
            ),
            re.compile(
                r"ORDONNE " + __multiple_words(0, 2) + TENANT_REGEX + " de payer son loyer le 1er de chaque mois",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_ordered_to_pay_landlord", [
            re.compile(
                r"CONDAMNE " + __multiple_words(0, 2) + TENANT_REGEX + " " + __multiple_words(0, 4) + r"à payer "
                + __multiple_words(0, 2) + LANDLORD_REGEX + r" la somme de " + MONEY_REGEX,
                re.IGNORECASE
            ),
        ], "MONEY_REGEX"),
        ("tenant_ordered_to_pay_landlord_legal_fees", [
            re.compile(
                r"(CONDAMNE " + __multiple_words(0, 2) + TENANT_REGEX + " " + __multiple_words(0, 3) + r"à payer "
                + __multiple_words(0, 2) + LANDLORD_REGEX + r".*)\Kplus les frais judiciaires de " + MONEY_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                r"CONDAMNE " + __multiple_words(0, 2) + TENANT_REGEX + " à payer aux locateurs \Kles frais "
                                                                       "judiciaires de " + MONEY_REGEX, re.IGNORECASE
            ),
            re.compile(
                r"frais judiciaires et de signification de " + MONEY_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                r"les frais judiciaires de " + MONEY_REGEX,
                re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("landlord_prejudice_justified", [
            re.compile(
                r".+(cause.+)?préjudice(causé)?.+(" +
                LANDLORD_REGEX +
                r"|demanderesse)?(justifie.+décision|sérieux)",
                re.IGNORECASE
            ),
            re.compile(
                r".+préjudice subi justifie",
                re.IGNORECASE
            ),
            re.compile(
                r".+le préjudice causé " + __multiple_words(0, 2) + LANDLORD_REGEX + r" justifie",
                re.IGNORECASE
            ),
            re.compile(
                r".+suffise.*" + TENANT_REGEX + r".*article 1863",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_retakes_apartment_indemnity", [
            re.compile(
                r".+compenser.+frais.+déménagement",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("authorize_landlord_retake_apartment", [
            re.compile(
                r"AUTORISE " + __multiple_words(0,
                                                2) + LANDLORD_REGEX + r" à reprendre (possession )?(du|le|des|de leur|de son) " +
                "(logement|lieu|lieux)",
                re.IGNORECASE
            )
        ], "BOOLEAN")
    ]

    model = {
        'regex_facts': regex_facts,
        'regex_outcomes': regex_outcomes,
        'MONEY_REGEX': MONEY_REGEX,
        'DATE_REGEX': DATE_REGEX
    }
