# -*- coding: utf-8 -*-
import re


class RegexLib:
    MONEY = r"(\d+(\s|,)){1,4}(\s\$|\$)"
    FACT_DIGIT_REGEX = r"\[\d+\]"
    DEMAND_DIGIT_REGEX = r"\[[123]\]"
    TENANT_REGEX = r"locataire(s)?"
    LANDLORD_REGEX = r"locat(eur|rice)(s)?"
    DEMAND_REGEX = r"(demand|réclam)(ait|e|ent|aient)"

    def multiple_words(min, max):
        return r"(\w+(\s|'|,\s)){" + str(min) + "," + str(max) + "}"

    regex_demands = [
        ("demand_lease_modification",
         [
             re.compile(
                 DEMAND_DIGIT_REGEX + r".+produit une demande en modifications du bail",
                 re.IGNORECASE
             )
         ], "BOOLEAN"),
        ("demand_resiliation", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + DEMAND_REGEX + r" la résiliation du bail",
                re.IGNORECASE
            ),
            re.compile(
                DEMAND_DIGIT_REGEX + r".+une demande en résiliation de bail",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_claim_interest_damage", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX +
                r".*" + MONEY + r".*dommages-intérêts",
                re.IGNORECASE
            )
        ], "MONEY"),
        ("landlord_demand_access_rental", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+accès au logement",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_demand_bank_fee", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+recouvrement.*frais\sbancaire(s)?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_demand_damage", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX +
                r".+" + DEMAND_REGEX + r".+dommage(s)?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_demand_legal_fees", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + DEMAND_REGEX +
                r"+.*remboursement.+(frais)?judiciaires",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_demand_retake_apartment", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".*" +
                DEMAND_REGEX + r".+(autoris(er|ation)).+reprendre.+logement",
                re.IGNORECASE
            ),
            re.compile(
                DEMAND_DIGIT_REGEX +
                r".+autorisation de reprendre le logement occupé par (le|la|les) " +
                TENANT_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                DEMAND_DIGIT_REGEX +
                r".+autorisation de reprendre le logement (du |de la |des )?(" +
                TENANT_REGEX + r" )?pour (s'|)y loger",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_demand_utility_fee", [
            re.compile(
                DEMAND_DIGIT_REGEX +
                r".+recouvrement(.+frais.+(énergie|électricité))+",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_fix_rent", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX +
                r".+" + DEMAND_REGEX + r".+(fix(er|ation)).+loyer",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_lease_termination", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".*.+résiliation.+bail",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_money_cover_rent", [
            re.compile(
                DEMAND_DIGIT_REGEX +
                r".+recouvrement (de loyer|du loyer|d'une somme|montant).+" + multiple_words(0, 3) + r"\s" + MONEY,
                re.IGNORECASE
            ),
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + DEMAND_REGEX + r" " + MONEY + r"de loyer",
                re.IGNORECASE
            ),
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + DEMAND_REGEX +
                r" du loyer impayé" + multiple_words(0, 3) +
                r"\s" + r"\(" + MONEY + r"\)",
                re.IGNORECASE
            )
        ], "MONEY"),
        ("paid_judicial_fees", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX +
                r"\s" + DEMAND_REGEX + r"+.+(frais\sjudiciaires)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_claims_harassment", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX +
                r".+(" + DEMAND_REGEX + r").+dommages.+harcèlement",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_cover_rent", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+(" + DEMAND_REGEX + r"+.+)?" + LANDLORD_REGEX +
                r"(s)?(.+" + DEMAND_REGEX + r"+)?.+recouvrement\s(du|de)\sloyer",
                re.IGNORECASE
            )
        ], 'BOOLEAN'),
        ("tenant_demands_decision_retraction", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX + r".+" +
                DEMAND_REGEX + r".+rétractation.+décision",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_demand_indemnity_Code_Civil", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX +
                r".*demande.*(Code\scivil\sdu\sQuébec)",
                re.IGNORECASE
            )
        ], 'BOOLEAN'),
        ("tenant_demand_indemnity_damage", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX +
                r".*(l'indemnité\sadditionnelle)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_demand_indemnity_judicial_fee", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX +
                r".+(recouvrement\sdes\sfrais\sjudiciaires)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_demand_interest_damage", [
            re.compile(
                DEMAND_DIGIT_REGEX +
                r".+(" + TENANT_REGEX + r").*" +
                DEMAND_REGEX + r"+.*(dommages-intérêts)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_demands_money", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX +
                r".+(" + DEMAND_REGEX + r").+" + MONEY,
                re.IGNORECASE
            )
        ], "MONEY"),
        ("tenant_demand_rent_decrease", [
            re.compile(
                DEMAND_DIGIT_REGEX +
                r".+(" + TENANT_REGEX + r").*" +
                DEMAND_REGEX + r".*diminution.*loyer",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_respect_of_contract", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + TENANT_REGEX +
                r".*(exécution\sen\snature\sd'une\sobligation)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_eviction", [
            re.compile(
                DEMAND_DIGIT_REGEX + r".+" + LANDLORD_REGEX +
                r".*(expulsion|éviction).*" + TENANT_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN")
    ]

    # TODO "tenant_request_cancel_lease", "tenant_pay_before_judgment",
    # "landlord_not_prejudice_justified", "tenant_claims_harm",
    # "tenant_is_asshole"
    regex_facts = [
        ("absent", [
            re.compile(
                FACT_DIGIT_REGEX +
                r".+considérant l'absence (du|de la|des) (" +
                LANDLORD_REGEX + r"|" + TENANT_REGEX + r")",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("apartment_impropre", [
            re.compile(
                FACT_DIGIT_REGEX +
                r".+(logement(était\s)?(.+impropre|infesté).+l'habitation|(bon\sétat.+propreté))",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+preuve.*logement.*" +
                TENANT_REGEX + r".*est.*mauvais.*état",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("apartment_infestation", [
            # FIXME
            # re.compile(
            #     FACT_DIGIT_REGEX + r".+infestation(s)?|\brat(s)?|fourmi(s)?|coquerelle(s)?|souri(s)?|excrément(s)?",
            #     re.IGNORECASE
            # )
        ], "BOOLEAN"),
        ("asker_is_landlord", [
            re.compile(
                DEMAND_DIGIT_REGEX + \
                r".+l(es|e|a) " + LANDLORD_REGEX + r" " + DEMAND_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("asker_is_tenant", [
            re.compile(
                DEMAND_DIGIT_REGEX + \
                r".+l(es|e|a) " + TENANT_REGEX + r" " + DEMAND_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("bothers_others", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r" trouble(nt|) la jouissance normale des lieux loués",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+dérange la jouissance paisible",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("case_fee_reimbursement", [
            re.compile(
                FACT_DIGIT_REGEX + r".+remboursement.+frais\sjudiciaires.+" + \
                MONEY,
                re.IGNORECASE
            )
        ], "MONEY"),
        ("disrespect_previous_judgement", [
            re.compile(
                FACT_DIGIT_REGEX + r".+non-respect d'une ordonnance émise antérieurement",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+pas respecté l'ordonnance de payer " + \
                multiple_words(0, 4) + r"loyer",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+non-respect de l'ordonnance de payer le loyer",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" " + \
                multiple_words(0, 3) + r"pas respecté l'ordonnance",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("incorrect_facts", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+demande (de la|des) " + TENANT_REGEX + r" est mal fondée",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_inspector_fees", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + \
                r".+(frais\sde\sdépistage)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_notifies_tenant_retake_apartment", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r".+" + \
                TENANT_REGEX + r".+(reprendre|reprise).+logement",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_pays_indemnity", [
            re.compile(
                FACT_DIGIT_REGEX + r".+dédommage.+" + TENANT_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_prejudice_justified", [
            re.compile(
                FACT_DIGIT_REGEX + r".+(cause.+)?préjudice(causé)?.+(" + \
                LANDLORD_REGEX + \
                r"|demanderesse)?(justifie.+décision|sérieux)",
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
        ], "BOOLEAN"),
        ("landlord_relocation_indemnity_fees", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+(" + LANDLORD_REGEX + r")?.+réclame.+indemnité.*" + MONEY,
                re.IGNORECASE
            )
        ], "MONEY"),
        ("landlord_rent_change", [
            re.compile(
                FACT_DIGIT_REGEX + r".+l'ajustement.+loyer",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_rent_change_doc_renseignements", [
            re.compile(
                FACT_DIGIT_REGEX + r".+formulaire\s(r|R)enseignements.+loyer",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_rent_change_piece_justification", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+formulaire\s(r|R)enseignements.+loyer.+(pièces\sjustificatives)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_rent_change_receipts", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+formulaire\s(r|R)enseignements.+loyer.+(pièces\sjustificatives).+factures",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_retakes_apartment", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + \
                r".+(reprendre|reprise)(.+logement)?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_retakes_apartment_indemnity", [
            re.compile(
                FACT_DIGIT_REGEX + r".+compenser.+frais.+déménagement",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_sends_demand_regie_logement", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + \
                r".+demande.+(Régie\sdu\slogement)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_serious_prejudice", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+cause un préjudice sérieux au(x|) " + LANDLORD_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r" " + \
                multiple_words(0, 1) + r"}un préjudice sérieux",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("lease", [
            re.compile(
                FACT_DIGIT_REGEX + r".+un bail " + \
                multiple_words(0, 8) + r"au loyer " + \
                multiple_words(0, 8) + r"mensuel de " + MONEY,
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".*bail valide.*loyer.*" + \
                MONEY + r"\spar mois",
                re.IGNORECASE)
        ], "MONEY"),
        ("proof_of_late", [
            re.compile(
                FACT_DIGIT_REGEX + r".+une reconnaissance de dette",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("proof_of_revenu", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+a fourni (\w+\s){0,10}l'attestation de ses revenu",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("rent_increased", [
            re.compile(
                FACT_DIGIT_REGEX + r".+preuve démontre la réception de l'avis d'augmentation",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_bad_payment_habits", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+(retard(s)?.+)?(loyer.+)?(payé|paient|paiement)(.+loyer)?(.+retard(s)?)?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_continuous_late_payment", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+(fréquen(ce|ts)).*(retard(s)?)?.*(article\s1971)?",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r" paie(nt|) (\w+\s){0,4}loyer(s|) (\w+\s){0,4}en retard",
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
        ], "BOOLEAN"),
        ("tenant_damaged_rental", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r" (a|ont) causé des dommages",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_dead", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r" (est|sont) décédé(e|s|es)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_declare_insalubre", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+(" + TENANT_REGEX + r".+)?(apartment.+)?insalubre",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_financial_problem", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+(" + TENANT_REGEX + \
                r".+)?difficultés.+financières(.+" + TENANT_REGEX + r")?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_group_responsability", [
            re.compile(
                FACT_DIGIT_REGEX + r".+bail.+(prévoit\spas).+" + TENANT_REGEX + \
                r".+(solidairement\sresponsables).+" + LANDLORD_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_individual_responsability", [
            re.compile(
                FACT_DIGIT_REGEX + r".+bail.+(prévoit).+" + TENANT_REGEX + \
                r".+(solidairement\sresponsables).+" + LANDLORD_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_is_bothered", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+(le|la|les) " + TENANT_REGEX + \
                r" (a|ont) subi(ent|) une perte de jouissance",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
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
        ], "BOOLEAN"),
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
                FACT_DIGIT_REGEX + r".+homologue " + \
                multiple_words(0, 3) + r"transaction",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_lease_fixed", [
            # FIXME
            # re.compile(
            #     FACT_DIGIT_REGEX + r".+((bail.*(reconduit.*)?(terminant.*)?((\d+?\w*?\s+?|)(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s+\d{2,4}|))((.+au|.*terminant).*(\d+?\w*?\s+?|)(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s+\d{2,4}|))?)|(fixation\sde\sloyer))",
            #     re.IGNORECASE
            # )
        ], 'BOOLEAN'),
        ("tenant_lease_indeterminate", [
            re.compile(
                FACT_DIGIT_REGEX + r".+bail.+durée\sindéterminée",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_left_without_paying", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+suite au déguerpissement (des|de la|du) " + \
                TENANT_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + r" " + \
                multiple_words(0, 6) + \
                r"(a|ont|aurait|auraient) quitté le logement",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r" (a|ont|aurait|auraient) quitté les lieux loué",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r" (a|ont) déguerpi (du logement|des lieux loué)",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+l'article 1975",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+suite du (départ|déguerpissement) (de la|du|des) " + \
                TENANT_REGEX,
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_monthly_payment", [
            re.compile(
                FACT_DIGIT_REGEX + r".+loyer\smensuel.*" + MONEY,
                re.IGNORECASE
            )
        ], "MONEY"),
        ("tenant_negligence", [
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+(causé par la|dû à la|vu la|en raison de la|à cause de la) négligence de la " + TENANT_REGEX,
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_not_request_cancel_lease", [
            re.compile(
                FACT_DIGIT_REGEX + r".+jamais.+(résiliation\sde\sbail)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_owes_rent", [
            # FIXME or SPLIT
            # re.compile(
            #     FACT_DIGIT_REGEX + r".+(.*preuve.+" + LANDLORD_REGEX + r".+non-paiement.+loyer)?.*(" + TENANT_REGEX + r".+(doi(vent|t))((.+somme\sde)|(total))?.+([\d\s,]+)(\$|\s\$)|" + LANDLORD_REGEX + r".+créance.+" + MONEY_REGEX + r".+loyers\simpayés)|(.*paiement.*arriérés.+loyer.+\b(\d{1,3}(\s\d{3}|,\d{2})*))",
            #     re.IGNORECASE
            # ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r" doi(ven|)t " + multiple_words(0, 6) + r"" + MONEY,
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + LANDLORD_REGEX + r" réclame(nt|) " + multiple_words(
                    0, 6) + r"" + MONEY + r"(, soit le loyer| à titre de loyer)",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+(il|elle)(s|) doi(ven)t toujours une somme de " + MONEY,
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+admet devoir la somme de " + \
                MONEY + r" à titre de loyer",
                re.IGNORECASE
            )
        ], "MONEY"),
        ("tenant_refuses_retake_apartment", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r".+refus(e|ait|aient).+quitter",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_rent_not_paid_less_3_weeks", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r".+pas.+retard.+(trois\ssemaines).+paiement.+loyer",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_rent_not_paid_more_3_weeks", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r".+retard.+plus.+((trois semaines)|(trois \(3\) semaines)).+(paiement\sdu\sloyer)",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r" (est|sont) en retard " + \
                multiple_words(1, 8) + r"(trois|3) semaines",
                re.IGNORECASE
            )

        ], "BOOLEAN"),
        ("tenant_rent_paid_before_hearing", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r".*payé.*loyer.*(dû le jour|avant).+(audience)",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + \
                r".+(ont|a|ayant) payé (le|tous les) loyer(s|) (dû|du)",
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
        ], "BOOLEAN"),
        ("tenant_violence", [
            re.compile(
                # FIXME
                FACT_DIGIT_REGEX + r".+(raison.+)?.*(viol(ent|ence))",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_withold_rent_without_permission", [
            re.compile(
                FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
                r".+ne peut.+faire justice.+retenir.+loyer.+(sans.+Tribunal)?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("violent", [
            re.compile(
                FACT_DIGIT_REGEX + r".+violentée|violent(e)?|menaçant(e)?",
                re.IGNORECASE
            ),
            re.compile(
                FACT_DIGIT_REGEX + r".+menace " + \
                multiple_words(
                    0, 6) + r"(sécurité des occupants|l'intégrité du logement)",
                re.IGNORECASE
            )
        ], "BOOLEAN")
    ]

    def get_regexes(self, name):
        for fact in RegexLib.regex_facts:
            if fact[0] == name:
                return fact[1]
        for demand in RegexLib.regex_demands:
            if demand[0] == name:
                return demand[1]

        # if name was not found in demands or facts
        return None

    def regex_finder(self, sentence):
        """
        This function is used to see if a regex is already written for a given sentence
        :param sentence: is used to find a regex the matches it
        :return: list of regex names that matches this sentence
        """
        regex_name_index = 0
        regex_index = 1
        regex_match_list = []

        for fact in RegexLib.regex_facts:
            for reg in fact[regex_index]:
                if re.search(reg, sentence):
                    regex_match_list.append(fact[regex_name_index])
        for demand in RegexLib.regex_demands:
            for reg in demand[regex_index]:
                if re.search(reg, sentence):
                    regex_match_list.append(demand[regex_name_index])

        return regex_match_list

    def sentence_finder(self, regex_name, nb_of_files):
        """
        finds sentences that matches the regex_name
        :param regex_name: name of the regex ex: landlord_money_cover_rent
        :param nb_of_files: number of files to search through
        :return: list of sentences that matched this regex
        """
        from util.file import Path
        import os
        regexes = self.get_regexes(regex_name)
        count = 0
        sentences_matched = []
        for i in os.listdir(Path.raw_data_directory):
            if count > nb_of_files:
                break
            count += 1
            file = open(Path.raw_data_directory + i, "r", encoding="ISO-8859-1")
            for line in file:
                for reg in regexes:
                    if reg.search(line):
                        sentences_matched.append(line)
            file.close()
        return sentences_matched

if "__main__" == __name__:
    import joblib
    regexes = RegexLib()
    dict = {}
    dict['regex_demands'] = regexes.regex_demands
    dict['regex_facts'] = regexes.regex_facts
    dict['MONEY'] = regexes.MONEY
    joblib.dump(dict, open("regexes.bin", "wb"))
