import re


class RegexLib:
    regex_list =[

    ]

    regex_demands = {
        "tenant_eviction": re.compile(r"(locateur|locatrice).+demande.+résiliation.+bail(.+(expulsion|éviction).+locataires)?"),
        "landlord_lease_termination": re.compile(r"(demande.+)?(locateur|locatrice).+résiliation.+bail"),
        "tenant_cover_rent": re.compile(r"(demande.+)?locateur(.+demande)?.+recouvrement\s(du|de)\sloyer"),
        "paid_judicial_fees": re.compile(r"(locateur|locatrice)\sdemande.+(frais\sjudiciaires)"),
        "landlord_money_cover_rent": re.compile(r"(locateur|locatrice)\sdemande.+recouvrement\s(du|de)\sloyer"),
        "landlord_fix_rent": re.compile(r"(locateur|locatrice)(s)?.+(demandent).+fixer.+loyer"),
        "tenant_demands_money": re.compile(r"locataire.+(demand(ait|ent)).+([\d\s]+)(\$|\s\$)"),
        "tenant_claims_harassment": re.compile(r"locataire.+(demand(ait|ent)).+dommages.+harcèlement"),
        "landlord_demand_utility_fee": re.compile(r"recouvrement(.+frais.+(énergie|électricité))+"),
        "landlord_demand_legal_fees": re.compile(r"remboursement.+(frais)?judiciaires"),
        "landlord_demand_bank_fee": re.compile(r"recouvrement.+frais\sbancaires"),
        "landlord_demand_retake_apartment": re.compile(r"(locateur|locatrice)(s)?.+demand(e|ent).+(autoris(er|ation)).+reprendre.+logement")
    }

    regex_facts = {
        "tenant_lease_indeterminate": re.compile(r"bail.+(durée\sindéterminée)"),
        "tenant_lease_fixed": re.compile(r"bail\s(reconduit\s|initial\s|ayant\sdébuté.+)?(pour.+période\s)?(de\s\d+\s(mois|ans).+)?(de\ssous-location\s)?(du|(et\s)?se\sterminant).+(au)?(.+\d{4})"),
        "tenant_monthly_payment": re.compile(r"loyer\smensuel\sde([\d\s,]+)(\$|\s\$)"),
        "tenant_owes_rent": re.compile(r"(locataire(s)?\sdoivent(.+somme\sde)?([\d\s,]+)(\$|\s\$)|locateur.+créance.+([\d\s,]+)(\$|\s\$).+loyers\simpayés)"),
        "tenant_rent_not_paid_more_3_weeks": re.compile(r"locataire(s)?.+retard.+plus.+trois\ssemaines.+(paiement\sdu\sloyer)"),
        "tenant_violence": re.compile(r"(comportement\s)?violent"),
        "tenant_request_cancel_lease": re.compile(r""),
        "tenant_not_request_cancel_lease": re.compile(r"jamais.+(résiliation\sde\sbail)"),
        "tenant_pay_before_judgment": re.compile(r""),
        "tenant_group_responsability": re.compile(r"bail.+(prévoit\spas).+locataire(s)?.+(solidairement\sresponsables).+locateur"),
        "tenant_individual_responsability": re.compile(r"bail.+(prévoit).+locataire(s)?.+(solidairement\sresponsables).+locateur"),
        "tenant_withold_rent_without_permission": re.compile(r"locataire(s)?.+(ne\speut).+(faire\sjustice).+retenir.+loyer.+(sans.+Tribunal)?"),
        "landlord_prejudice_justified": re.compile(r"(cause.+)?préjudice(causé)?.+(locateur|locatrice|demanderesse)?(justifie.+décision|sérieux)"),
        "landlord_not_prejudice_justified": re.compile(r""),
        "tenant_bad_payment_habits": re.compile(r"(retard(s)?.+)?(loyer.+)?(payé|paient|paiement)(.+loyer)?(.+retard(s)?)?"),
        "tenant_financial_problem": re.compile(r"(locataire(s)?.+)?difficultés.+financières(.+locataire(s)?)?"),
        "landlord_rent_change": re.compile(r"l'ajustement\sdu\sloyer"),
        "landlord_rent_change_doc_renseignements": re.compile(r"formulaire\s(r|R)enseignements.+loyer"),
        "landlord_rent_change_piece_justification": re.compile(r"formulaire\s(r|R)enseignements.+loyer.+(pièces\sjustificatives)"),
        "landlord_rent_change_receipts": re.compile(r"formulaire\s(r|R)enseignements.+loyer.+(pièces\sjustificatives).+factures"),
        "tenant_lacks_proof": re.compile(r"considérant\sl'absence.+\;"),
        "landlord_retakes_apartment": re.compile(r""),
        "landlord_notifies_tenant_retake_apartment": re.compile(r"(locateur|locatrice)(s)?.+locataire(s)?.+(reprendre|reprise).+logement"),
        "tenant_refuses_retake_apartment": re.compile(r"locataire(s)?.+refus(e|ait|aient).+quitter"),
        "landlord_sends_demand_regie_logement": re.compile(r"(locateur|locatrice)(s)?.+demande.+(Régie\sdu\slogement)"),
        "tenant_claims_harm": re.compile(r""),
        "landlord_retakes_apartment_indemnity": re.compile(r"compenser.+frais.+déménagement")
    }