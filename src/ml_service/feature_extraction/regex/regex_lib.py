import re


class RegexLib:
    regex_list =[

    ]

    regex_demands = {
        "tenant_eviction": re.compile(r"(locateur|locatrice).+demande.+résiliation.+bail.+expulsion.+locataires"),
        "landlord_lease_termination": re.compile(r"(demande.+)?(locateur|locatrice).+résiliation.+bail"),
        "tenant_cover_rent": re.compile(r"(demande.+)?locateur(.+demande)?.+recouvrement\s(du|de)\sloyer"),
        "paid_judicial_fees": re.compile(r"(locateur|locatrice)\sdemande.+(frais\sjudiciaires)"),
        "landlord_money_cover_rent": re.compile(r"(locateur|locatrice)\sdemande.+recouvrement\s(du|de)\sloyer")
    }

    regex_facts = {

    }