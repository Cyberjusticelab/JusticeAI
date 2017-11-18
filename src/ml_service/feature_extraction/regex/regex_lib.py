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
        "tenant_lease_fixed": re.compile(r"bail\s(reconduit\s)?(du|se\sterminant).+au(.+\d{4})"),
        "tenant_monthly_payment": re.compile(r"loyer\smensuel\sde([\d\s]+)(\$|\s\$)"),
        "tenant_owes_rent": re.compile(r"(locataire(s)?\sdoivent([\d\s]+)(\$|\s\$)|locateur.+créance.+([\d\s]+)(\$|\s\$).+loyers\simpayés)"),
        "tenant_rent_not_paid_more_3_weeks": re.compile(r"locataire(s)?.+retard.+plus.+trois\ssemaines.+(paiement\sdu\sloyer)"),
        "tenant_violence": re.compile(r"comportement\sviolent"),
        "tenant_request_cancel_lease": re.compile(r""),
        "tenant_not_request_cancel_lease": re.compile(r"jamais.+(résiliation\sde\sbail)"),
        "tenant_pay_before_judgment": re.compile(r""),
        "tenant_group_responsability": re.compile(r"bail.+(prévoit\spas).+locataire(s)?.+(solidairement\sresponsables).+locateur"),
        "tenant_individual_responsability": re.compile(r""),
        "tenant_withold_rent_without_permission": re.compile(r"locataire(s)?.+(ne\speut).+(faire\sjustice).+retenir.+loyer.+(sans.+Tribunal)?"),
        "landlord_prejudice_justified": re.compile(r"préjudice.+(causé)?.+(locateur|locatrice).+justifie.+décision"),
        "landlord_not_prejudice_justified": re.compile(r"")
    }