# -*- coding: utf-8 -*-
import re


class RegexLib:
    MONEY_REGEX = r"(\d+(\s|,)){1,4}(\s\$|\$)"
    FACT_DIGIT_REGEX = r"\[\d+\]"
    DEMAND_DIGIT_REGEX = r"\[[123]\]"
    TENANT_REGEX = r"locataire(s)?"
    LANDLORD_REGEX = r"locat(eur|rice)(s)?"
    DEMAND_REGEX = r"(demand|réclam)(ait|e|ent|aient)"

    def multiple_words(min, max):
        return r"(\w+(\s|'|,\s)){"+ str(min) + ","+ str(max) +"}"

    regex_demands = [
        ("demand_lease_modification", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+produit une demande en modifications du bail",
                re.IGNORECASE
            )
        ]),
        ("demand_resiliation", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + DEMAND_REGEX + r" la résiliation du bail",
                re.IGNORECASE
            ),
            re.compile(
                DEMAND_DIGIT_REGEX + r".+une demande en résiliation de bail",
                re.IGNORECASE
            )
        ]),
        ("landlord_claim_interest_damage", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".*" + MONEY_REGEX + r".*dommages-intérêts",
                re.IGNORECASE
            )
        ]),
        ("landlord_demand_access_rental", [
         re.compile(
             DEMAND_DIGIT_REGEX + r".+accès au logement",
             re.IGNORECASE
         )
         ]),
        ("landlord_demand_bank_fee", [
         re.compile(
             DEMAND_DIGIT_REGEX + r".+recouvrement.*frais\sbancaire(s)?",
             re.IGNORECASE
         )
         ]),
        ("landlord_demand_damage", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".+" + DEMAND_REGEX + r".+dommage(s)?",
                re.IGNORECASE
            )
        ]),
        ("landlord_demand_legal_fees", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + DEMAND_REGEX + r"+.*remboursement.+(frais)?judiciaires",
                re.IGNORECASE
            )
        ]),
        ("landlord_demand_retake_apartment", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".*" + DEMAND_REGEX + r".+(autoris(er|ation)).+reprendre.+logement",
                re.IGNORECASE
            ),
            re.compile(
                DEMAND_DIGIT_REGEX + r".+autorisation de reprendre le logement occupé par (le|la|les) " + TENANT_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                DEMAND_DIGIT_REGEX + r".+autorisation de reprendre le logement (du |de la |des )?(" + TENANT_REGEX + r" )?pour (s'|)y loger",
                re.IGNORECASE
            )
        ]),
        ("landlord_demand_utility_fee", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+recouvrement(.+frais.+(énergie|électricité))+",
                re.IGNORECASE
            )
        ]),
        ("landlord_fix_rent", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".+" + DEMAND_REGEX + r".+(fix(er|ation)).+loyer",
                re.IGNORECASE
            )
        ]),
        ("landlord_lease_termination", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".*.+résiliation.+bail",
                re.IGNORECASE
            )
        ]),
        ("landlord_money_cover_rent", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".+" + DEMAND_REGEX + r"?.+recouvrement.+\sloyer",
                re.IGNORECASE
            ),
            re.compile(
                DEMAND_DIGIT_REGEX + r".+recouvrement (de loyer|du loyer|d'une somme)",
                re.IGNORECASE
            ),
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + DEMAND_REGEX + r" " + MONEY_REGEX + r"de loyer",
                re.IGNORECASE
            ),
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + DEMAND_REGEX + r" du loyer impayé",
                re.IGNORECASE
            )
        ]),
        ("paid_judicial_fees", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r"\s" + DEMAND_REGEX + r"+.+(frais\sjudiciaires)",
                re.IGNORECASE
            )
        ]),
        ("tenant_claims_harassment", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX + r".+(" + DEMAND_REGEX + r").+dommages.+harcèlement",
                re.IGNORECASE
            )
        ]),
        ("tenant_cover_rent", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+(" + DEMAND_REGEX + r"+.+)?" + LANDLORD_REGEX + r"(s)?(.+" + DEMAND_REGEX + r"+)?.+recouvrement\s(du|de)\sloyer",
                re.IGNORECASE
            )
        ]),
        ("tenant_demands_decision_retraction", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX + r".+" + DEMAND_REGEX + r".+rétractation.+décision",
                re.IGNORECASE
            )
        ]),
        ("tenant_demand_indemnity_Code_Civil", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX + r".*demande.*(Code\scivil\sdu\sQuébec)",
                re.IGNORECASE
            )
        ]),
        ("tenant_demand_indemnity_damage", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX + r".*(l'indemnité\sadditionnelle)",
                re.IGNORECASE
            )
        ]),
        ("tenant_demand_indemnity_judicial_fee", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r".+(recouvrement\sdes\sfrais\sjudiciaires)",
                re.IGNORECASE
            )
        ]),
        ("tenant_demand_interest_damage", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+(" + TENANT_REGEX + r").*" + DEMAND_REGEX + r"+.*(dommages-intérêts)",
                re.IGNORECASE
            )
        ]),
        ("tenant_demands_money", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX + r".+(" + DEMAND_REGEX + r").+" + MONEY_REGEX,
                re.IGNORECASE
            )
        ]),
        ("tenant_demand_rent_decrease", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+(" + TENANT_REGEX + r").*" + DEMAND_REGEX + r".*diminution.*loyer",
                re.IGNORECASE
            )
        ]),
        ("tenant_respect_of_contract", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX + r".*(exécution\sen\snature\sd'une\sobligation)",
                re.IGNORECASE
            )
        ]),
        ("tenant_eviction", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".*(expulsion|éviction).*" + TENANT_REGEX + r"",
                re.IGNORECASE
            )
        ])
    ]

    # TODO "tenant_request_cancel_lease", "tenant_pay_before_judgment",
    # "landlord_not_prejudice_justified", "tenant_claims_harm",
    # "tenant_is_asshole"
    regex_facts = [
        ("absent", [
            re.compile(
                FACT_DIGIT_REGEX + r".+considérant l'absence (du|de la|des) (" + LANDLORD_REGEX + r"|" + TENANT_REGEX + r")",
                re.IGNORECASE
            )
        ]),
        ("apartment_impropre", [
            re.compile(
                FACT_DIGIT_REGEX + r".+(logement(était\s)?(.+impropre|infesté).+l'habitation|(bon\sétat.+propreté))",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+preuve.*logement.*" + TENANT_REGEX + r".*est.*mauvais.*état",
                re.IGNORECASE
            )
        ]),
        ("apartment_infestation", [
            re.compile(
                FACT_DIGIT_REGEX + r".+infestation(s)?|rat(s)?|fourmi(s)?|coquerelle(s)?|souri(s)?|excrément(s)?",
                re.IGNORECASE
            )
        ]),
        ("asker_is_landlord", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+l(es|e|a) " + LANDLORD_REGEX + r" " + DEMAND_REGEX + r"",
                re.IGNORECASE
            )
        ]),
        ("asker_is_tenant", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+l(es|e|a) " + TENANT_REGEX + r" " + DEMAND_REGEX + r"",
                re.IGNORECASE
            )
        ]),
        ("bothers_others", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" trouble(nt|) la jouissance normale des lieux loués",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+dérange la jouissance paisible",
                re.IGNORECASE
            )
        ]),
        ("disrespect_previous_judgement", [
            re.compile(
                FACT_DIGIT_REGEX + r".+non-respect d'une ordonnance émise antérieurement",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+pas respecté l'ordonnance de payer " + multiple_words(0,4) + r"loyer",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+non-respect de l'ordonnance de payer le loyer",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" " + multiple_words(0,3) + r"pas respecté l'ordonnance",
                re.IGNORECASE
            )
        ]),
        ("incorrect_facts", [
            re.compile(
                FACT_DIGIT_REGEX + r".+demande (de la|des) " + TENANT_REGEX + r" est mal fondée",
                re.IGNORECASE
            )
        ]),
        ("landlord_inspector_fees", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".+(frais\sde\sdépistage)",
                re.IGNORECASE
            )
        ]),
        ("landlord_notifies_tenant_retake_apartment", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".+" + TENANT_REGEX + r".+(reprendre|reprise).+logement",
                re.IGNORECASE
            )
        ]),
        ("landlord_pays_indemnity", [
         re.compile(
             FACT_DIGIT_REGEX + r".+dédommage.+" + TENANT_REGEX + r"",
             re.IGNORECASE
         )
         ]),
        ("landlord_prejudice_justified", [
            re.compile(
                FACT_DIGIT_REGEX + r".+(cause.+)?préjudice(causé)?.+(" + LANDLORD_REGEX + r"|demanderesse)?(justifie.+décision|sérieux)",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+préjudice subi justifie",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+le préjudice causé au " + LANDLORD_REGEX + r" justifie",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+suffise.*" + TENANT_REGEX + r".*article 1863",
                re.IGNORECASE
            )
        ]),
        ("landlord_relocation_indemnity_fees", [
            re.compile(
                FACT_DIGIT_REGEX + r".+(" + LANDLORD_REGEX + r")?.+réclame.+indemnité.*" + MONEY_REGEX,
                re.IGNORECASE
            )
        ]),
        ("landlord_rent_change", [
         re.compile(
             FACT_DIGIT_REGEX + r".+l'ajustement.+loyer",
             re.IGNORECASE
         )
         ]),
        ("landlord_rent_change_doc_renseignements", [
         re.compile(
             FACT_DIGIT_REGEX + r".+formulaire\s(r|R)enseignements.+loyer",
             re.IGNORECASE
         )
         ]),
        ("landlord_rent_change_piece_justification", [
            re.compile(
                FACT_DIGIT_REGEX + r".+formulaire\s(r|R)enseignements.+loyer.+(pièces\sjustificatives)",
                re.IGNORECASE
            )
        ]),
        ("landlord_rent_change_receipts", [
            re.compile(
                FACT_DIGIT_REGEX + r".+formulaire\s(r|R)enseignements.+loyer.+(pièces\sjustificatives).+factures",
                re.IGNORECASE
            )
        ]),
        ("landlord_retakes_apartment", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".+(reprendre|reprise)(.+logement)?",
                re.IGNORECASE
            )
        ]),
        ("landlord_retakes_apartment_indemnity", [
         re.compile(
             FACT_DIGIT_REGEX + r".+compenser.+frais.+déménagement",
             re.IGNORECASE
         )
         ]),
        ("landlord_sends_demand_regie_logement", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".+demande.+(Régie\sdu\slogement)",
                re.IGNORECASE
            )
        ]),
        ("landlord_serious_prejudice", [
            re.compile(
                FACT_DIGIT_REGEX + r".+cause un préjudice sérieux au(x|) " + LANDLORD_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r" " + multiple_words(0,1) + r"}un préjudice sérieux",
                re.IGNORECASE
            )
        ]),
        ("lease", [
            re.compile(
                FACT_DIGIT_REGEX + r".+un bail " + multiple_words(0,8) + r"au loyer " + multiple_words(0,8) + r"mensuel de " + MONEY_REGEX,
                re.IGNORECASE
            )
        ]),
        ("proof_of_late", [
         re.compile(
             FACT_DIGIT_REGEX + r".+une reconnaissance de dette",
             re.IGNORECASE
         )
         ]),
        ("proof_of_revenu", [
            re.compile(
                FACT_DIGIT_REGEX + r".+a fourni (\w+\s){0,10}l'attestation de ses revenu",
                re.IGNORECASE
            )
        ]),
        ("rent_increased", [
            re.compile(
                FACT_DIGIT_REGEX + r".+preuve démontre la réception de l'avis d'augmentation",
                re.IGNORECASE
            )
        ]),
        ("tenant_bad_payment_habits", [
            re.compile(
                FACT_DIGIT_REGEX + r".+(retard(s)?.+)?(loyer.+)?(payé|paient|paiement)(.+loyer)?(.+retard(s)?)?",
                re.IGNORECASE
            )
        ]),
        ("tenant_continuous_late_payment", [
            re.compile(
                FACT_DIGIT_REGEX + r".+(fréquen(ce|ts)).*(retard(s)?)?.*(article\s1971)?",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" paie(nt|) (\w+\s){0,4}loyer(s|) (\w+\s){0,4}en retard",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+preuve de retards fréquents dans le paiement du loyer",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+considérant la preuve des retards fréquents",
                re.IGNORECASE
            )
        ]),
        ("tenant_damaged_rental", [
         re.compile(
             FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" (a|ont) causé des dommages",
             re.IGNORECASE
         )
         ]),
        ("tenant_dead", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" (est|sont) décédé(e|s|es)",
                re.IGNORECASE
            )
        ]),
        ("tenant_declare_insalubre", [
         re.compile(
             FACT_DIGIT_REGEX + r".+(" + TENANT_REGEX + r".+)?(apartment.+)?insalubre",
             re.IGNORECASE
         )
         ]),
        ("tenant_financial_problem", [
            re.compile(
                FACT_DIGIT_REGEX + r".+(" + TENANT_REGEX + r".+)?difficultés.+financières(.+" + TENANT_REGEX + r")?",
                re.IGNORECASE
            )
        ]),
        ("tenant_group_responsability", [
            re.compile(
                FACT_DIGIT_REGEX + r".+bail.+(prévoit\spas).+" + TENANT_REGEX + r".+(solidairement\sresponsables).+" + LANDLORD_REGEX + r"",
                re.IGNORECASE
            )
        ]),
        ("tenant_individual_responsability", [
            re.compile(
                FACT_DIGIT_REGEX + r".+bail.+(prévoit).+" + TENANT_REGEX + r".+(solidairement\sresponsables).+" + LANDLORD_REGEX + r"",
                re.IGNORECASE
            )
        ]),
        ("tenant_is_bothered", [
            re.compile(
                FACT_DIGIT_REGEX + r".+(le|la|les) " + TENANT_REGEX + r" (a|ont) subi(ent|) une perte de jouissance",
                re.IGNORECASE
            )
        ]),
        ("lack_of_proof", [
            re.compile(
                FACT_DIGIT_REGEX + r".+considérant\sl'absence de preuve",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+absence de preuve",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+aucune preuve au soutien de la demande",
                re.IGNORECASE
            )
        ]),
        ("tenant_landlord_agreement", [
            re.compile(
                FACT_DIGIT_REGEX + r".+entente.+(entre\sles\sdeux\sparties)",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+entérine (l'|cette\s)entente",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+l'entente intervenue entre les parties",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+homologue cette entente",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+homologue " + multiple_words(0,3) + r"transaction",
                re.IGNORECASE
            )
        ]),
        ("tenant_lease_fixed", [
            # FIXME
            # re.compile(
            #     FACT_DIGIT_REGEX + r".+((bail.*(reconduit.*)?(terminant.*)?((\d+?\w*?\s+?|)(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s+\d{2,4}|))((.+au|.*terminant).*(\d+?\w*?\s+?|)(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s+\d{2,4}|))?)|(fixation\sde\sloyer))",
            #     re.IGNORECASE
            # )
        ]),
        ("tenant_lease_indeterminate", [
         re.compile(
             FACT_DIGIT_REGEX + r".+bail.+durée\sindéterminée",
             re.IGNORECASE
         )
         ]),
        ("tenant_left_without_paying", [
            re.compile(
                FACT_DIGIT_REGEX + r".+suite au déguerpissement (des|de la|du) " + TENANT_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" " + multiple_words(0,6) + r"(a|ont|aurait|auraient) quitté le logement",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" (a|ont|aurait|auraient) quitté les lieux loué",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" (a|ont) déguerpi (du logement|des lieux loué)",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+l'article 1975",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+suite du (départ|déguerpissement) (de la|du|des) " + TENANT_REGEX,
                re.IGNORECASE
            )
        ]),
        ("tenant_monthly_payment", [
            re.compile(
                FACT_DIGIT_REGEX + r".+loyer\smensuel.*" + MONEY_REGEX,
                re.IGNORECASE
            )
        ]),
        ("tenant_negligence", [
            re.compile(
                FACT_DIGIT_REGEX + r".+(causé par la|dû à la|vu la|en raison de la|à cause de la) négligence de la " + TENANT_REGEX,
                re.IGNORECASE
            )
        ]),
        ("tenant_not_request_cancel_lease", [
         re.compile(
             FACT_DIGIT_REGEX + r".+jamais.+(résiliation\sde\sbail)",
             re.IGNORECASE
         )
         ]),
        ("tenant_owes_rent", [
            # FIXME or SPLIT
            # re.compile(
            #     FACT_DIGIT_REGEX + r".+(.*preuve.+" + LANDLORD_REGEX + r".+non-paiement.+loyer)?.*(" + TENANT_REGEX + r".+(doi(vent|t))((.+somme\sde)|(total))?.+([\d\s,]+)(\$|\s\$)|" + LANDLORD_REGEX + r".+créance.+" + MONEY_REGEX + r".+loyers\simpayés)|(.*paiement.*arriérés.+loyer.+\b(\d{1,3}(\s\d{3}|,\d{2})*))",
            #     re.IGNORECASE
            # ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" doi(ven|)t " + multiple_words(0,6) + r"" + MONEY_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r" réclame(nt|) " + multiple_words(0,6) + r"" + MONEY_REGEX + r"(, soit le loyer| à titre de loyer)",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+(il|elle)(s|) doi(ven)t toujours une somme de " + MONEY_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+admet devoir la somme de " + MONEY_REGEX + r" à titre de loyer",
                re.IGNORECASE
            )
        ]),
        ("tenant_refuses_retake_apartment", [
         re.compile(
             FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r".+refus(e|ait|aient).+quitter",
             re.IGNORECASE
         )
         ]),
        ("tenant_rent_not_paid_less_3_weeks", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r".+pas.+retard.+(trois\ssemaines).+paiement.+loyer",
                re.IGNORECASE
            )
        ]),
        ("tenant_rent_not_paid_more_3_weeks", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r".+retard.+plus.+((trois semaines)|(trois \(3\) semaines)).+(paiement\sdu\sloyer)",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" (est|sont) en retard " + multiple_words(1,8) + r"(trois|3) semaines",
                re.IGNORECASE
            )

        ]),
        ("tenant_rent_paid_before_hearing", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r".*payé.*loyer.*(dû le jour|avant).+(audience)",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+(ont|a|ayant) payé (le|tous les) loyer(s|) (dû|du)",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+(ont|a) payé les loyers réclamés",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+les loyers ont été payés",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+à la date de l'audience, tous les loyers réclamés ont été payés",
                re.IGNORECASE
            )
        ]),
        ("tenant_violence", [
         re.compile(
             # FIXME
             FACT_DIGIT_REGEX + r".+(raison.+)?.*(viol(ent|ence))",
             re.IGNORECASE
         )
         ]),
        ("tenant_withold_rent_without_permission", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r".+ne peut.+faire justice.+retenir.+loyer.+(sans.+Tribunal)?",
                re.IGNORECASE
            )
        ]),
        ("violent", [
            re.compile(
                FACT_DIGIT_REGEX + r".+violentée|violent(e)?|menaçant(e)?",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+menace " + multiple_words(0,6) + r"(sécurité des occupants|l'intégrité du logement)",
                re.IGNORECASE
            )
        ])
    ]

    def get_regexes(name):
        for fact in RegexLib.regex_facts:
            if fact[0] == name:
                return fact[1]
        for demand in RegexLib.regex_demands:
            if demand[0] == name:
                return demand[1]

        # if name was not found in demands or facts
        return None
