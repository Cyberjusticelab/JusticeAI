# -*- coding: utf-8 -*-
import regex as re


class RegexLib:
    MONEY_REGEX = r"(\d+(\s|,)){1,4}(\s\$|\$)"
    TENANT_REGEX = r"locataire(s)?"
    LANDLORD_REGEX = r"locat(eur|rice)(s)?"
    DEMAND_REGEX = r"(demand|réclam)(ait|e|ent|aient)"
    DATE_REGEX = r"(janvier|février|mars|avril|d'avril|mai|juin|juillet|d'août|août|septembre|d'octobre|octobre|novembre|décembre)"

    def __multiple_words(min, max):
        return r"([a-zA-ZÀ-ÿ0-9]+(\s|'|,\s)){" + str(min) + "," + str(max) + "}"

    # #############################################################
    # DEMANDS
    # #############################################################

    regex_demands = [
        ("demand_lease_modification",
         [
             re.compile(
                 r".+produit une demande en modifications du bail",
                 re.IGNORECASE
             )
         ], "BOOLEAN"),
        ("demand_resiliation", [
            re.compile(
                r".+" + DEMAND_REGEX + r" la résiliation du bail",
                re.IGNORECASE
            ),
            re.compile(
                r".+une demande en résiliation de bail",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_claim_interest_damage", [
            re.compile(
                r".+" + LANDLORD_REGEX +
                r".*" + MONEY_REGEX + r".*dommages-intérêts",
                re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("landlord_demand_access_rental", [
            re.compile(
                r".+accès au logement",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_demand_bank_fee", [
            re.compile(
                r".+recouvrement.*\K" + MONEY_REGEX + r"\spour\s(les\s|des\s)?frais\sbancaire(s)?",
                re.IGNORECASE
            ),
            re.compile(
                r".+recouvrement.*\K" + MONEY_REGEX + r"\s\(frais\sbancaire(s)?\)",
                re.IGNORECASE
            ),
            re.compile(
                r".+recouvrement.*\Kfrais\sbancaire(s)?\s(de\s)?" +
                r"(\()?" + MONEY_REGEX + r"(\))?",
                re.IGNORECASE
            ),
        ], "MONEY_REGEX"),
        ("landlord_demand_damage", [
            re.compile(
                r".+" + LANDLORD_REGEX +
                r".+" + DEMAND_REGEX + r".+dommage(s)?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_demand_legal_fees", [
            re.compile(
                r".+" + DEMAND_REGEX +
                r"+.*remboursement.+(frais)?judiciaires",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_demand_retake_apartment", [
            re.compile(
                r".+" + LANDLORD_REGEX + r".*" +
                DEMAND_REGEX + r".+(autoris(er|ation)).+reprendre.+logement",
                re.IGNORECASE
            ),
            re.compile(
                r".+autorisation de reprendre le logement occupé par (le|la|les) " +
                TENANT_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                r".+autorisation de reprendre le logement (du |de la |des )?(" +
                TENANT_REGEX + r" )?pour (s'|)y loger",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_demand_utility_fee", [
            re.compile(
                r".*\K" + MONEY_REGEX + r"\s(((pour|représentant)\s(les\s|des\s)?)|en\s)?\(?frais\s(d'énergie|d'électricité|hydroélectricité)\)?",
                re.IGNORECASE
            ),
            re.compile(
                r".*\Kfrais\s(d'énergie|d'électricité|hydroélectricité)\s((au montant\s)?de\s)?" +
                r"\(?" + MONEY_REGEX + r"\)?",
                re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("landlord_fix_rent", [
            re.compile(
                r".+" + LANDLORD_REGEX +
                r".+" + DEMAND_REGEX + r".+(fix(er|ation)).+loyer",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_lease_termination", [
            re.compile(
                r".+" + LANDLORD_REGEX + r".*.+résiliation.+bail",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_money_cover_rent", [
            re.compile(
                r".+recouvrement (de loyer|du loyer|d'une somme|montant).+" + __multiple_words(0, 3) + r"\s" + MONEY_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                r".+" + DEMAND_REGEX + r" " + MONEY_REGEX + r"de loyer",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + DEMAND_REGEX +
                r" du loyer impayé" + __multiple_words(0, 3) +
                r"\s" + r"\(" + MONEY_REGEX + r"\)",
                re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("paid_judicial_fees", [
            re.compile(
                r".+" + LANDLORD_REGEX +
                r"\s" + DEMAND_REGEX + r"+.+(frais\sjudiciaires)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_claims_harassment", [
            re.compile(
                r".+" + TENANT_REGEX +
                r".+(" + DEMAND_REGEX + r").+dommages.+harcèlement",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_cover_rent", [
            re.compile(
                r".+(" + DEMAND_REGEX + r"+.+)?" + LANDLORD_REGEX +
                r"(s)?(.+" + DEMAND_REGEX + r"+)?.+recouvrement\s(du|de)\sloyer",
                re.IGNORECASE
            )
        ], 'BOOLEAN'),
        ("tenant_demands_decision_retraction", [
            re.compile(
                r".+" + TENANT_REGEX + r".+" +
                DEMAND_REGEX + r".+rétractation.+décision",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_demand_indemnity_Code_Civil", [
            re.compile(
                r".+" + TENANT_REGEX +
                r".*demande.*(Code\scivil\sdu\sQuébec)",
                re.IGNORECASE
            )
        ], 'BOOLEAN'),
        ("tenant_demand_indemnity_damage", [
            re.compile(
                r".+" + TENANT_REGEX +
                r".*(l'indemnité\sadditionnelle)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_demand_indemnity_judicial_fee", [
            re.compile(
                r".+" + TENANT_REGEX +
                r".+(recouvrement\sdes\sfrais\sjudiciaires)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_demand_interest_damage", [
            re.compile(
                r".+(" + TENANT_REGEX + r").*" +
                DEMAND_REGEX + r"+.*(dommages-intérêts)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_demands_money", [
            re.compile(
                r".+" + TENANT_REGEX +
                r".+(" + DEMAND_REGEX + r").+" + MONEY_REGEX,
                re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("tenant_demand_rent_decrease", [
            re.compile(
                r".+(" + TENANT_REGEX + r").*" +
                DEMAND_REGEX + r".*diminution.*loyer",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_respect_of_contract", [
            re.compile(
                r".+" + TENANT_REGEX +
                r".*(exécution\sen\snature\sd'une\sobligation)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("case_fee_reimbursement", [
            re.compile(
                r".+remboursement.+frais\sjudiciaires.+" + \
                MONEY_REGEX,
                re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("tenant_eviction", [
            re.compile(
                r".+" + LANDLORD_REGEX +
                r".*(expulsion|éviction).*" + TENANT_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN")
    ]

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
                r".+preuve.*logement.*" +
                TENANT_REGEX + r".*est.*mauvais.*état",
                re.IGNORECASE
            ),
            re.compile(
                r".+((infestation(s)?|traitement)\s(soudaine et imprévue )?de (punaise(s)?|rat(s)?|fourmi(s)?|coquerelle(s)?|souri(s))|excrément(s)?)",
                re.IGNORECASE
            ),
            re.compile(
                r".+(" + TENANT_REGEX + r".+)?(apartment.+)?insalubre",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("asker_is_landlord", [
            re.compile(
                r".+l(es|e|a) " + LANDLORD_REGEX + r" " + DEMAND_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("asker_is_tenant", [
            re.compile(
                r".+l(es|e|a) " + TENANT_REGEX + r" " + DEMAND_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("bothers_others", [
            re.compile(
                r".+" + TENANT_REGEX + \
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
                r".+" + TENANT_REGEX + \
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
                r".+pas respecté l'ordonnance de payer " + \
                __multiple_words(0, 4) + r"loyer",
                re.IGNORECASE
            ),
            re.compile(
                r".+non-respect de l'ordonnance de payer le loyer",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + TENANT_REGEX + r" " + \
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
                r".+" + LANDLORD_REGEX + r".+" + \
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
                r".+(" + LANDLORD_REGEX + r")?.+réclame.+indemnité de relocation\s" + __multiple_words(0, 5) + MONEY_REGEX,
                re.IGNORECASE
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
                r".+" + LANDLORD_REGEX + \
                r".+(reprendre|reprise)(.+logement)?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("landlord_sends_demand_regie_logement", [
            re.compile(
                r".+" + LANDLORD_REGEX + \
                r".+demande.+ordonnance.+(Régie\sdu\slogement)",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + LANDLORD_REGEX + \
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
                TENANT_REGEX + r".+au " + LANDLORD_REGEX + \
                r" une mise en demeure.+(demanderait|demande).+Régie du logement",
                re.IGNORECASE
            ),
            re.compile(
                TENANT_REGEX + r" envoie une mise en demeure au " + LANDLORD_REGEX + \
                r".+ (demanderait|demande) .+ Régie du logement",
                re.IGNORECASE
            ),
            re.compile(
                TENANT_REGEX + r" demande à la Régie du logement",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_lease_fixed", [
            re.compile(
                r".+un bail " + \
                __multiple_words(0, 8) + r"au loyer " + \
                __multiple_words(0, 8) + r"mensuel de " + MONEY_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                r".*bail valide.*loyer.*" + \
                MONEY_REGEX + r"\spar mois",
                re.IGNORECASE)
        ], "MONEY_REGEX"),
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
                r".+" + TENANT_REGEX + \
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
                r".+" + TENANT_REGEX + \
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
                r".+" + TENANT_REGEX + \
                r" (est|sont) décédé(e|s|es)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_financial_problem", [
            re.compile(
                r".+(" + TENANT_REGEX + \
                r".+)?difficultés.+financières(.+" + TENANT_REGEX + r")?",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_group_responsability", [
            re.compile(
                r".+bail.+(prévoit\spas).+" + TENANT_REGEX + \
                r".+(solidairement\sresponsables).+" + LANDLORD_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_individual_responsability", [
            re.compile(
                r".+bail.+(prévoit).+" + TENANT_REGEX + \
                r".+(solidairement\sresponsables).+" + LANDLORD_REGEX + r"",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_is_bothered", [
            re.compile(
                \
                r".+(le|la|les) " + TENANT_REGEX + \
                r" (a|ont) subi(ent|) une perte de jouissance",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_lease_fixed", [
            # FIXME
            # re.compile(
            #     r".+((bail.*(reconduit.*)?(terminant.*)?((\d+?\w*?\s+?|)(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s+\d{2,4}|))((.+au|.*terminant).*(\d+?\w*?\s+?|)(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s+\d{2,4}|))?)|(fixation\sde\sloyer))",
            #     re.IGNORECASE
            # )
            re.compile(
                r".+un bail " + \
                __multiple_words(0, 8) + r"au loyer " + \
                __multiple_words(0, 8) + r"mensuel de " + MONEY_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                r".*bail valide.*loyer.*" + \
                MONEY_REGEX + r"\spar mois",
                re.IGNORECASE)
        ], 'MONEY_REGEX'),
        ("tenant_lease_indeterminate", [
            re.compile(
                r".+bail.+durée\sindéterminée",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_left_without_paying", [
            re.compile(
                r".+suite au déguerpissement (des|de la|du) " + \
                TENANT_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + TENANT_REGEX + r" " + \
                __multiple_words(0, 6) + \
                r"(a|ont|aurait|auraient) quitté le logement",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + TENANT_REGEX + \
                r" (a|ont|aurait|auraient) quitté les lieux loué",
                re.IGNORECASE
            ),
            re.compile(
                r".+" + TENANT_REGEX + \
                r" (a|ont) déguerpi (du logement|des lieux loué)",
                re.IGNORECASE
            ),
            re.compile(
                r".+l'article 1975",
                re.IGNORECASE
            ),
            re.compile(
                r".+suite du (départ|déguerpissement) (de la|du|des) " + \
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
        ("tenant_rent_not_paid_less_3_weeks", [
            re.compile(
                r".+" + TENANT_REGEX + \
                r".+pas.+retard.+(trois\ssemaines).+paiement.+loyer",
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
            re.compile(
                r".+violentée|violent(e)?|menaçant(e)?",
                re.IGNORECASE
            ),
            re.compile(
                r".+menace " + \
                __multiple_words(
                    0, 6) + r"(sécurité des occupants|l'intégrité du logement)",
                re.IGNORECASE
            ),
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
        ("not_violent",[
            re.compile(
                r".+\sn('|e\s)" + __multiple_words(1, 5) +
                                   r"(violen(ce|t(e|é)?)(s)?|(l')?agressi(f|ve|vité)|mena(ce(s)?|çant(s)?)"
                                   r"|vulgaire|intimida(tion|nt)(s)?|hostile|inadéquat)",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_not_paid_lease_timespan",[
            re.compile(
                DATE_REGEX + r".+n'est pas payé",
                re.IGNORECASE
            ),
            re.compile(
                TENANT_REGEX + r" pas payé.+" + DATE_REGEX + r".+et" + DATE_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                TENANT_REGEX + r" n'a pas payé le loyer " + DATE_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                "le loyer de " + DATE_REGEX + " \d{0,4} n'est toujours pas payé",
                re.IGNORECASE
            ),
            re.compile(
                "pas payé le(s|) loyer(s|) du(s|) pour le(s|) mois (de |)" + DATE_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                r"pas payé(s|) au(x|) " + LANDLORD_REGEX + r" le(s|) loyer(s|) (du|des) mois (de|)" + DATE_REGEX
            )
        ], 'DATE_REGEX')
    ]

    # #############################################################
    # OUTCOMES
    # #############################################################

    regex_outcomes = [
        ("additional_indemnity_money", [
            re.compile(
                r"(l'|)indemnité additionnelle prévue à l'article 1619 C\.c\.Q\., à compter du \d{0,2}(er|èr|" + \
                r"ere|em|eme|ème)? " + DATE_REGEX + " \d{0,4} sur la somme de " + MONEY_REGEX,
                re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("declares_housing_inhabitable", [
            re.compile(
                r"DÉCLARE le logement impropre à l'habitation",
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
                r"préjudice sérieux au(x|) " + LANDLORD_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                r"préjudice sérieux à la " + LANDLORD_REGEX + r"",
                re.IGNORECASE
            ),
            re.compile(
                LANDLORD_REGEX + r" " + \
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
                "caus(e|ent) au(x|) " + LANDLORD_REGEX + r" un préjudice sérieux",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("orders_expulsion", [
            re.compile(
                r"ORDONNE l'expulsion"
            ),
            re.compile(
                r"ORDONNE au(x|) " + TENANT_REGEX + " et à tous les occupants du logement de quitter les lieux",
                re.IGNORECASE
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
                r"ORDONNE (au|à la|aux) " + TENANT_REGEX + " de payer le loyer le premier jour",
                re.IGNORECASE
            ),
            re.compile(
                r"ORDONNE (au|à la|aux) " + TENANT_REGEX + " de payer ses loyers à échoir le premier jour de chaque mois",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("tenant_ordered_to_pay_landlord", [
            re.compile(
                r"CONDAMNE le(s)? " + TENANT_REGEX + " " + __multiple_words(0, 3) + r"à payer (au|à la|aux) " +
                LANDLORD_REGEX + r" la somme de " + MONEY_REGEX,
                re.IGNORECASE
            )
        ], "MONEY_REGEX"),
        ("tenant_ordered_to_pay_landlord_legal_fees", [
            re.compile(
                r"(CONDAMNE le(s)? " + TENANT_REGEX + " " + __multiple_words(0, 3) + r"à payer (au|à la|aux) " +
                LANDLORD_REGEX + r".*)\Kplus les frais judiciaires de " + MONEY_REGEX,
                re.IGNORECASE
            ),
            re.compile(
                r"CONDAMNE le locataire à payer aux locateurs \Kles frais judiciaires de " + MONEY_REGEX,
                re.IGNORECASE
            ),
        ], "MONEY_REGEX"),
        ("landlord_prejudice_justified", [
            re.compile(
                r".+(cause.+)?préjudice(causé)?.+(" + \
                LANDLORD_REGEX + \
                r"|demanderesse)?(justifie.+décision|sérieux)",
                re.IGNORECASE
            ),
            re.compile(
                r".+préjudice subi justifie",
                re.IGNORECASE
            ),
            re.compile(
                r".+le préjudice causé au " + LANDLORD_REGEX + r" justifie",
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
        ("orders_landlord_notify_tenant_when_habitable", [
            re.compile(
                r"ORDONNE au " + LANDLORD_REGEX + ".+d'aviser la locataire dès que le logement sera redevenu propre à l'habitation",
                re.IGNORECASE
            )
        ], "BOOLEAN"),
        ("authorize_landlord_retake_apartment", [
            re.compile(
                "AUTORISE (le|la|les) " + LANDLORD_REGEX + " à reprendre le logement ",
                re.IGNORECASE
            ),
            re.compile(
                "AUTORISE (le|la|les) " + LANDLORD_REGEX + " à reprendre possession du logement",
                re.IGNORECASE
            )
        ], "BOOLEAN")
    ]

    model = {
        'regex_demands': regex_demands,
        'regex_facts': regex_facts,
        'regex_outcomes': regex_outcomes,
        'MONEY_REGEX': MONEY_REGEX,
        'DATE_REGEX': DATE_REGEX
    }