import os
import re
import collections


def get_ask_resiliation():
    reg = re.compile('\[[123]\].+demande(nt|) la résiliation du bail')
    reg2 = re.compile('\[[123]\].+une demande en résiliation de bail')
    return meta_regex("Ask Resiliation", [reg, reg2])


def get_lease():
    reg = re.compile(
        '\[\d+\].+un bail (\w+(\s|\'|,\s)){0,8}au loyer (\w+(\s|\'|,\s)){0,8}mensuel de (\d+(\s|\,)){1,2}\$')
    return meta_regex("Lease", [reg])


def get_money_owed():
    reg = re.compile(
        '\[\d+\].+doi(ven|)t la somme de (\d+(\s|\,)){1,2}\$(, soit le loyer| à titre de loyer)')
    reg2 = re.compile(
        '\[\d+\].+locataire(s|) doi(ven|)t (\w+(\s|\'|,\s)){0,6}(\d+(\s|\,)){1,2}\$')
    reg3 = re.compile(
        '\[\d+\].+locat(eur|rice)(s|) réclame(nt|) (\w+(\s|\'|,\s)){0,6}(\d+(\s|\,)){1,2}\$(, soit le loyer| à titre de loyer)')
    reg4 = re.compile(
        '\[\d+\].+(il|elle)(s|) doi(ven)t toujours une somme de (\d+(\s|\,)){1,2}\$')
    reg5 = re.compile(
        '\[\d+\].+admet devoir la somme de (\d+(\s|\,)){1,2}\$ à titre de loyer')
    return meta_regex("Money Owed", [reg, reg2, reg3, reg4, reg5])


def get_non_respect_of_judgement():
    reg = re.compile(
        '\[\d+\].+non-respect d\'une ordonnance émise antérieurement')
    reg2 = re.compile(
        '\[\d+\].+pas respecté l\'ordonnance de payer (\w+(\s|\'|,\s)){0,4}loyer')
    reg3 = re.compile(
        '\[\d+\].+non-respect de l\'ordonnance de payer le loyer')
    reg4 = re.compile(
        '\[\d+\].+locataire(s|) (\w+(\s|\'|,\s)){0,3}pas respecté l\'ordonnance')
    return meta_regex("Disrespect previous judgement", [reg, reg2, reg3, reg4])


def get_menacing():
    reg = re.compile(
        '\[\d+\].+menace (\w+(\s|\'|,\s)){0,6}(sécurité des occupants|l\'intégrité du logement)')
    return meta_regex("Menacing", [reg])


def get_serious_prejudice():
    reg = re.compile(
        '\[\d+\].+cause un préjudice sérieux au(x|) locat(eur|rice)(s|)')
    reg2 = re.compile(
        '\[\d+\].+locat(eur|rice)(s|) (\w+(\s|\'|,\s)){0,10}un préjudice sérieux')
    reg3 = re.compile(
        '\[\d+\].+préjudice subi justifie')
    reg4 = re.compile(
        '\[\d+\].+Le préjudice causé au locateur justifie')
    return meta_regex("Landlord serious prejudice", [reg, reg2, reg3, reg4])


def get_late_payment():
    reg = re.compile(
        '\[\d+\].+locataire(s|) paie(nt|) (\w+\s){0,4}loyer(s|) (\w+\s){0,4}en retard')
    reg2 = re.compile(
        '\[\d+\].+preuve de retards fréquents dans le paiement du loyer')
    reg3 = re.compile(
        '\[\d+\].+CONSIDÉRANT la preuve des retards fréquents')

    return meta_regex("Often Late Payment", [reg, reg2, reg3])


def get_tenant_died():
    reg = re.compile('\[\d+\].+locataire(s|) (est|sont) décédé(e|s|es)')
    return meta_regex("Tenant dead", [reg])


def get_three_weeks_late():
    reg = re.compile(
        '\[\d+\].+locataire(s|) (est|sont) en retard (\w+(\s|\'|,\s)){1,8}(trois|3) semaines')
    return meta_regex("Is 3 week late", [reg])


def get_tenant_left():
    reg = re.compile(
        '\[\d+\].+locataire(s|) (\w+(\s|\'|,\s)){0,6}(a|ont|aurait|auraient) quitté le logement')
    reg2 = re.compile(
        '\[\d+\].+locataire(s|) (a|ont) quitté les lieux loué')
    reg3 = re.compile(
        '\[\d+\].+locataire(s|) (a|ont) déguerpi (du logement|des lieux loué)')
    return meta_regex("Tenant Left", [reg, reg2, reg3])


def get_tenant_negligence():
    reg = re.compile(
        '(causé par la|dû à la|vu la|en raison de la|à cause de la) négligence de la locataire')
    return meta_regex("Tenant Negligence", [reg])


def get_increased_rent():
    reg = re.compile(
        '\[\d+\].+preuve démontre la réception de l\'avis d\'augmentation')
    return meta_regex("Rent increase", [reg])


def get_proof_of_late():
    reg = re.compile('\[\d+\].+une reconnaissance de dette')
    return meta_regex("Proof of debt", [reg])


def get_no_rent_owed():
    reg = re.compile('aucun loyer n\'est dû')
    return meta_regex("No money owed", [reg])


def get_lack_of_proof():
    reg = re.compile('\[\d+\].+absence de preuve')
    reg2 = re.compile('\[\d+\].+aucune preuve au soutien de la demande')

    return meta_regex("Lack of proof", [reg, reg2])


def get_bothers_others():
    reg = re.compile(
        '\[\d+\].+locataire(s|) trouble(nt|) la jouissance normale des lieux loués')
    reg = re.compile(
        '\[\d+\].+dérange la jouissance paisible')
    return meta_regex("Tenant Bothers", [reg])


def get_tenat_is_bothered():
    reg = re.compile(
        '\[\d+\].+(le|la|les) locataire(s|) (a|ont) subi(ent|) une perte de jouissance')
    return meta_regex('Tenant is bothered', [reg])


def get_not_three_weeks_late():
    reg = re.compile(
        '\[\d+\].+locataire(s|) (n\'est|ne sont) pas en retard (\w+(\s|\'|,\s)){1,8}trois semaines')
    return meta_regex("Is Not 3 week late", [reg])


def get_tenant_damaged_rental():
    reg = re.compile('\[\d+\].+locataire (a|ont) causé des dommages')
    return meta_regex("Rental Damage", [reg])


def get_bad_mutual_agreement():
    reg = re.compile('\[\d+\].+ENTÉRINE (l\'|cette\s)entente')
    reg2 = re.compile('\[\d+\].+l\'entente intervenue entre les parties')
    reg3 = re.compile('\[\d+\].+HOMOLOGUE cette entente')
    reg4 = re.compile('\[\d+\].+HOMOLOGUE (\w+(\s|\'|,\s)){0,3}transaction')
    return meta_regex("BAD: Mutual Agreement", [reg, reg2, reg3, reg4])


def get_proof_of_revenu():
    reg = re.compile(
        '\[\d+\].+a fourni (\w+\s){0,10}l\'attestation de ses revenu')
    return meta_regex("Proof of revenu", [reg])


def get_bad_paid_before_audience():
    reg = re.compile(
        '\[\d+\].+(ont|a|ayant) payé (le|tous les) loyer(s|) (dû|du)')
    reg2 = re.compile('\[\d+\].+(ont|a) payé les loyers réclamés')
    reg3 = re.compile(
        '\[\d+\].+les loyers ont été payés')
    reg4 = re.compile(
        '\[\d+\].+à la date de l\'audience, tous les loyers réclamés ont été payés')

    return meta_regex("BAD: Paid Before Hearing", [reg, reg2, reg3, reg4])


def get_bad_absent():
    reg = re.compile(
        '\[\d+\].+CONSIDÉRANT l\'absence (du|de la|des) locat(eur|rice|aire)(s|)')
    return meta_regex("BAD: Absent", [reg])


def get_bad_incorrect_facts():
    reg = re.compile(
        '\[\d+\].+demande (de la|des) locataire(s|) est mal fondée')
    return meta_regex("BAD: Incorrect Facts", [reg])


def meta_regex(name, regexes):
    returnList = set()
    precFiles = os.listdir('precedents/text_bk')
    for file in precFiles:
        with open('precedents/text_bk/' + file, 'r', encoding="ISO-8859-1") as f:
            s = f.read()
            for reg in regexes:
                if reg.search(s):
                    returnList.add(file)
    print("% of precedents with {} : {}".format(name,
                                                len(returnList) * 100.0 / len(precFiles)))
    return returnList

get_lease()

ask_resiliation = get_ask_resiliation()
tenant_left = get_tenant_left()
late_payment = get_late_payment()
menacing = get_menacing()
three_weeks_late = get_three_weeks_late()
proof_of_late = get_proof_of_late()
increased_rent = get_increased_rent()
not_three_weeks_late = get_not_three_weeks_late()
lack_of_proof = get_lack_of_proof()
serious_prejudice = get_serious_prejudice()
money_owed = get_money_owed()
no_rent_owed = get_no_rent_owed()
proof_of_revenu = get_proof_of_revenu()
bothers_others = get_bothers_others()
non_respect_of_judgement = get_non_respect_of_judgement()
tenant_died = get_tenant_died()
tenant_damaged_rental = get_tenant_damaged_rental()
tenant_negligence = get_tenant_negligence()
tenant_is_bothered = get_tenat_is_bothered()

bad_mutual_agreement = get_bad_mutual_agreement()
bad_paid_before_audience = get_bad_paid_before_audience()
bad_absent = get_bad_absent()
bad_incorrect_facts = get_bad_incorrect_facts()

meta = money_owed.union(
    tenant_left).union(
    proof_of_revenu).union(
    late_payment).union(
    tenant_negligence).union(
    menacing).union(
    three_weeks_late).union(
    tenant_is_bothered).union(
    increased_rent).union(
    proof_of_late).union(
    not_three_weeks_late).union(
    lack_of_proof).union(
    serious_prejudice).union(
    tenant_damaged_rental).union(
    tenant_died).union(
    no_rent_owed).union(
    non_respect_of_judgement).union(
    bothers_others)

rem = ask_resiliation - bad_mutual_agreement - \
    bad_paid_before_audience - bad_absent - bad_incorrect_facts
inter = rem - meta.intersection(ask_resiliation)

print("Diff total:")
print(len(inter))

print("Diff %:")
print(len(inter) * 100.0 / len(rem))

with open('diff.txt', 'w') as file:
    for item in inter:
        file.write("%s\n" % item)
