import os
import re
import joblib
import src.ml_service.feature_extraction.regex.regex_lib


def get_asker_landlord():
    return meta_regex("asker is landlord", [
        re.compile(
            '\[[123]\].+l(es|e|a) locat(eur|rice)(s|) (demande|réclame)(nt|)', re.IGNORECASE)
    ])


def get_asker_tenant():
    return meta_regex("asker is tenant", [
        re.compile(
            '\[[123]\].+l(es|e|a) locataire(s|) (demande|réclame)(nt|)', re.IGNORECASE)
    ])


def get_asking_rent_payment():
    return meta_regex("ask for rent payment", [
        re.compile(
            '\[[123]\].+recouvrement (de loyer|du loyer|d\'une somme)', re.IGNORECASE),
        re.compile(
            '\[[123]\].+(demande|réclame)(nt|) ((\d+(\s|,)){0,3}(\$ |))de loyer', re.IGNORECASE),
        re.compile(
            '\[[123]\].+(demande|réclame)(nt|) du loyer impayé', re.IGNORECASE)
    ])


def get_ask_access_rental():
    return meta_regex("ask for access to rental", [
        re.compile('\[[123]\].+accès au logement')
    ])


def get_ask_fixation_of_rent():
    return meta_regex("ask fixing rent", [
        re.compile('\[[123]\].+fixation (du|de) loyer', re.IGNORECASE),
        re.compile(
            '\[[123]\].+fixer le loyer', re.IGNORECASE)
    ])


def get_ask_resiliation():
    return meta_regex("ask resiliation", [
        re.compile(
            '\[[123]\].+(demande|réclame)(nt|) la résiliation du bail', re.IGNORECASE),
        re.compile(
            '\[[123]\].+une demande en résiliation de bail', re.IGNORECASE)
    ])


def get_ask_lease_modification():
    return meta_regex("ask modification of lease", [
        re.compile(
            '\[[123]\].+produit une demande en modifications du bail', re.IGNORECASE)
    ])


def get_ask_lower_rent():
    return meta_regex("ask lower rent", [
        re.compile(
            '\[[123]\].+(demande|réclame)(nt|) (une|de|en) diminution de loyer', re.IGNORECASE)
    ])


def get_ask_retake_rental():
    return meta_regex("ask retake rental", [
        re.compile(
            '\[[123]\].+autorisation de reprendre le logement occupé par (le|la|les) locataire(s|)', re.IGNORECASE),
        re.compile(
            '\[[123]\].+autorisation de reprendre le logement (du locataire |de la locataire )pour (s\'|)y loger', re.IGNORECASE)
    ])


def get_ask_damages():
    return meta_regex("ask damages", [
        re.compile(
            '\[[123]\].+(demande|réclame)(nt|) ((\d+(\s|,)){0,3}(\$ |)){0,1}(en|de|des|pour des|pour de) dommage', re.IGNORECASE)
    ])

#done
def get_lease():
    return meta_regex("lease", [
        re.compile(
            '\[\d+\].+un bail (\w+(\s|\'|,\s)){0,8}au loyer (\w+(\s|\'|,\s)){0,8}mensuel de (\d+(\s|\,)){1,2}\$', re.IGNORECASE)
    ])

#done
def get_money_owed():
    return meta_regex("money owed", [
        re.compile(
            '\[\d+\].+doi(ven|)t la somme de (\d+(\s|\,)){1,2}\$(, soit le loyer| à titre de loyer)', re.IGNORECASE),
        re.compile(
            '\[\d+\].+locataire(s|) doi(ven|)t (\w+(\s|\'|,\s)){0,6}(\d+(\s|\,)){1,2}\$', re.IGNORECASE),
        re.compile(
            '\[\d+\].+locat(eur|rice)(s|) réclame(nt|) (\w+(\s|\'|,\s)){0,6}(\d+(\s|\,)){1,2}\$(, soit le loyer| à titre de loyer)', re.IGNORECASE),
        re.compile(
            '\[\d+\].+(il|elle)(s|) doi(ven)t toujours une somme de (\d+(\s|\,)){1,2}\$', re.IGNORECASE),
        re.compile(
            '\[\d+\].+admet devoir la somme de (\d+(\s|\,)){1,2}\$ à titre de loyer', re.IGNORECASE)
    ])

#done
def get_non_respect_of_judgement():
    return meta_regex("disrespect previous judgement", [
        re.compile(
            '\[\d+\].+non-respect d\'une ordonnance émise antérieurement', re.IGNORECASE),
        re.compile(
            '\[\d+\].+pas respecté l\'ordonnance de payer (\w+(\s|\'|,\s)){0,4}loyer', re.IGNORECASE),
        re.compile(
            '\[\d+\].+non-respect de l\'ordonnance de payer le loyer', re.IGNORECASE),
        re.compile(
            '\[\d+\].+locataire(s|) (\w+(\s|\'|,\s)){0,3}pas respecté l\'ordonnance', re.IGNORECASE)
    ])

# done
def get_menacing():
    return meta_regex("menacing", [
        re.compile(
            '\[\d+\].+menace (\w+(\s|\'|,\s)){0,6}(sécurité des occupants|l\'intégrité du logement)', re.IGNORECASE)
    ])


def get_serious_prejudice():
    return meta_regex("landlord serious prejudice", [
        re.compile(
            '\[\d+\].+cause un préjudice sérieux au(x|) locat(eur|rice)(s|)', re.IGNORECASE),
        re.compile(
            '\[\d+\].+locat(eur|rice)(s|) (\w+(\s|\'|,\s)){0,10}un préjudice sérieux', re.IGNORECASE),
        re.compile(
            '\[\d+\].+préjudice subi justifie', re.IGNORECASE),
        re.compile(
            '\[\d+\].+le préjudice causé au locateur justifie', re.IGNORECASE),
        re.compile(
            '\[\d+\].+suffise.*locataire.*article 1863', re.IGNORECASE)
    ])


def get_late_payment():
    return meta_regex("often late payment", [
        re.compile(
            '\[\d+\].+locataire(s|) paie(nt|) (\w+\s){0,4}loyer(s|) (\w+\s){0,4}en retard', re.IGNORECASE),
        re.compile(
            '\[\d+\].+preuve de retards fréquents dans le paiement du loyer', re.IGNORECASE),
        re.compile(
            '\[\d+\].+considérant la preuve des retards fréquents', re.IGNORECASE)
    ])


def get_tenant_died():
    return meta_regex("tenant dead", [
        re.compile(
            '\[\d+\].+locataire(s|) (est|sont) décédé(e|s|es)', re.IGNORECASE)
    ])


def get_three_weeks_late():
    return meta_regex("is 3 week late", [
        re.compile(
            '\[\d+\].+locataire(s|) (est|sont) en retard (\w+(\s|\'|,\s)){1,8}(trois|3) semaines', re.IGNORECASE)
    ])


def get_tenant_left():
    return meta_regex("tenant left", [
        re.compile(
            '\[\d+\].+locataire(s|) (\w+(\s|\'|,\s)){0,6}(a|ont|aurait|auraient) quitté le logement', re.IGNORECASE),
        re.compile(
            '\[\d+\].+locataire(s|) (a|ont) quitté les lieux loué', re.IGNORECASE),
        re.compile(
            '\[\d+\].+locataire(s|) (a|ont) déguerpi (du logement|des lieux loué)',
            re.IGNORECASE),
        re.compile(
            '\[\d+\].+l\'article 1975', re.IGNORECASE)
    ])


def get_tenant_negligence():
    return meta_regex("tenant negligence", [
        re.compile(
            '(causé par la|dû à la|vu la|en raison de la|à cause de la) négligence de la locataire', re.IGNORECASE)
    ])


def get_increased_rent():
    return meta_regex("rent increase", [
        re.compile(
            '\[\d+\].+preuve démontre la réception de l\'avis d\'augmentation', re.IGNORECASE)
    ])


def get_proof_of_late():
    return meta_regex("proof of debt", [
        re.compile('\[\d+\].+une reconnaissance de dette', re.IGNORECASE)
    ])


def get_no_rent_owed():
    return meta_regex("no money owed", [
        re.compile('\[\d+\].+aucun loyer n\'est dû', re.IGNORECASE)
    ])


def get_lack_of_proof():
    return meta_regex("lack of proof", [
        re.compile('\[\d+\].+absence de preuve', re.IGNORECASE),
        re.compile(
            '\[\d+\].+aucune preuve au soutien de la demande', re.IGNORECASE)
    ])


def get_bothers_others():
    return meta_regex("tenant bothers", [
        re.compile(
            '\[\d+\].+locataire(s|) trouble(nt|) la jouissance normale des lieux loués', re.IGNORECASE),
        re.compile(
            '\[\d+\].+dérange la jouissance paisible', re.IGNORECASE)
    ])


def get_is_not_habitable():
    return meta_regex('Is not habitable', [
        re.compile(
            '\[\d+\].+preuve.*logement.*locataire.*est.*mauvais.*état', re.IGNORECASE)
    ])


def get_tenant_is_bothered():
    return meta_regex('tenant is bothered', [
        re.compile(
            '\[\d+\].+(le|la|les) locataire(s|) (a|ont) subi(ent|) une perte de jouissance', re.IGNORECASE)
    ])


def get_not_three_weeks_late():
    return meta_regex("is not 3 week late", [
        re.compile(
            '\[\d+\].+locataire(s|) (n\'est|ne sont) pas en retard (\w+(\s|\'|,\s)){1,8}trois semaines', re.IGNORECASE)
    ])


def get_tenant_damaged_rental():
    return meta_regex("rental damage", [
        re.compile(
            '\[\d+\].+locataire (a|ont) causé des dommages', re.IGNORECASE)
    ])


def get_bad_mutual_agreement():
    return meta_regex("bad: mutual agreement", [
        re.compile('\[\d+\].+entérine (l\'|cette\s)entente', re.IGNORECASE),
        re.compile(
            '\[\d+\].+l\'entente intervenue entre les parties', re.IGNORECASE),
        re.compile('\[\d+\].+homologue cette entente', re.IGNORECASE),
        re.compile(
            '\[\d+\].+homologue (\w+(\s|\'|,\s)){0,3}transaction', re.IGNORECASE)
    ])


def get_proof_of_revenu():
    return meta_regex("proof of revenu", [
        re.compile(
            '\[\d+\].+a fourni (\w+\s){0,10}l\'attestation de ses revenu')
    ])


def get_bad_paid_before_audience():
    return meta_regex("bad: paid before hearing", [
        re.compile(
            '\[\d+\].+(ont|a|ayant) payé (le|tous les) loyer(s|) (dû|du)', re.IGNORECASE),
        re.compile(
            '\[\d+\].+(ont|a) payé les loyers réclamés', re.IGNORECASE),
        re.compile(
            '\[\d+\].+les loyers ont été payés', re.IGNORECASE),
        re.compile(
            '\[\d+\].+à la date de l\'audience, tous les loyers réclamés ont été payés', re.IGNORECASE)
    ])


def get_bad_absent():
    return meta_regex("bad: absent", [
        re.compile(
            '\[\d+\].+considérant l\'absence (du|de la|des) locat(eur|rice|aire)(s|)', re.IGNORECASE)
    ])


def get_bad_incorrect_facts():
    return meta_regex("bad: incorrect facts", [
        re.compile(
            '\[\d+\].+demande (de la|des) locataire(s|) est mal fondée', re.IGNORECASE)
    ])


def meta_regex(name, regex):
    returnlist = set()
    precfiles = os.listdir('precedents/text_bk')
    for file in precfiles:
        with open('precedents/text_bk/' + file, 'r', encoding="iso-8859-1") as f:
            s = f.read()
            if regex[0].search(s):
                returnlist.add(file)
    print("Percent of precedents with {} : {}".format(name, len(returnlist) * 100.0 / len(precfiles)))
    return returnlist


def fill_dict(precedentDict, fileSet, fact):
    for precedent in precedentDict.keys():
        if precedent in fileSet:
            precedentDict[precedent][fact] = 1
        else:
            precedentDict[precedent][fact] = 0


lease = get_lease()
asker_landlord = get_asker_landlord()
asker_tenant = get_asker_tenant()
ask_lease_modification = get_ask_lease_modification()
ask_retake_rental = get_ask_retake_rental()
ask_lower_rent = get_ask_lower_rent()
ask_damages = get_ask_damages()
ask_fixation_of_rent = get_ask_fixation_of_rent()
asking_rent_payment = get_asking_rent_payment()
ask_access_rental = get_ask_access_rental()

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
tenant_is_bothered = get_tenant_is_bothered()
is_not_habitable = get_is_not_habitable()

bad_mutual_agreement = get_bad_mutual_agreement()
bad_paid_before_audience = get_bad_paid_before_audience()
bad_absent = get_bad_absent()
bad_incorrect_facts = get_bad_incorrect_facts()

meta = money_owed.union(
    tenant_left).union(
    is_not_habitable).union(
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


all_precedents = set(os.listdir('precedents/text_bk'))
bad_precedents = bad_mutual_agreement.union(
    bad_paid_before_audience).union(bad_absent).union(bad_incorrect_facts)
good_precedents = all_precedents - bad_precedents
precedent_vector = dict((el, {}) for el in good_precedents)


fill_dict(precedent_vector, lease, 'lease')
fill_dict(precedent_vector, asker_landlord, 'asker_landlord')
fill_dict(precedent_vector, asker_tenant, 'asker_tenant')
fill_dict(precedent_vector, ask_lease_modification, 'ask_lease_modification')
fill_dict(precedent_vector, ask_retake_rental, 'ask_retake_rental')
fill_dict(precedent_vector, ask_lower_rent, 'ask_lower_rent')
fill_dict(precedent_vector, ask_damages, 'ask_damages')
fill_dict(precedent_vector, ask_fixation_of_rent, 'ask_fixation_of_rent')
fill_dict(precedent_vector, asking_rent_payment, 'asking_rent_payment')
fill_dict(precedent_vector, ask_access_rental, 'ask_access_rental')
fill_dict(precedent_vector, ask_resiliation, 'ask_resiliation')
fill_dict(precedent_vector, tenant_left, 'tenant_left')
fill_dict(precedent_vector, late_payment, 'late_payment')
fill_dict(precedent_vector, menacing, 'menacing')
fill_dict(precedent_vector, three_weeks_late, 'three_weeks_late')
fill_dict(precedent_vector, proof_of_late, 'proof_of_late')
fill_dict(precedent_vector, increased_rent, 'increased_rent')
fill_dict(precedent_vector, not_three_weeks_late, 'not_three_weeks_late')
fill_dict(precedent_vector, lack_of_proof, 'lack_of_proof')
fill_dict(precedent_vector, serious_prejudice, 'serious_prejudice')
fill_dict(precedent_vector, money_owed, 'money_owed')
fill_dict(precedent_vector, no_rent_owed, 'no_rent_owed')
fill_dict(precedent_vector, proof_of_revenu, 'proof_of_revenu')
fill_dict(precedent_vector, bothers_others, 'bothers_others')
fill_dict(precedent_vector, non_respect_of_judgement,'non_respect_of_judgement')
fill_dict(precedent_vector, tenant_died, 'tenant_died')
fill_dict(precedent_vector, tenant_damaged_rental, 'tenant_damaged_rental')
fill_dict(precedent_vector, tenant_negligence, 'tenant_negligence')
fill_dict(precedent_vector, tenant_is_bothered, 'tenant_is_bothered')
fill_dict(precedent_vector, is_not_habitable, 'is_not_habitable')

joblib.dump(precedent_vector, 'prec.bin')

print("diff total:")
print(len(inter))

print("diff %:")
print(len(inter) * 100.0 / len(rem))

with open('diff.txt', 'w') as file:
    for item in inter:
        file.write("%s\n" % item)
