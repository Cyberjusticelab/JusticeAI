import os
import re
import joblib
from feature_extraction.regex.regex_lib import RegexLib

regex_lib = RegexLib()


def get_ask_lease_modification():
    return meta_regex("ask modification of lease", [
        re.compile(
            '\[[123]\].+produit une demande en modifications du bail', re.IGNORECASE)
    ])


def get_not_three_weeks_late():
    return meta_regex("is not 3 week late", [
        re.compile(
            '\[\d+\].+locataire(s|) (n\'est|ne sont) pas en retard (\w+(\s|\'|,\s)){1,8}trois semaines', re.IGNORECASE)
    ])


def meta_regex(name, regexes):
    returnlist = set()
    precfiles = os.listdir('precedents/text_bk')
    for file in precfiles:
        with open('precedents/text_bk/' + file, 'r', encoding="iso-8859-1") as f:
            s = f.read()
            for reg in regexes:
                if reg.search(s):
                    returnlist.add(file)
    print("Percent of precedents with {} : {}".format(name,
                                                len(returnlist) * 100.0 / len(precfiles)))
    return returnlist


def fill_dict(precedentDict, fileSet, fact):
    for precedent in precedentDict.keys():
        if precedent in fileSet:
            precedentDict[precedent][fact] = 1
        else:
            precedentDict[precedent][fact] = 0


def get_matching_precedent_file_names(fact):
    return meta_regex(fact, regex_lib.get_regexes(fact))

lease = get_matching_precedent_file_names("lease")
asker_landlord = get_matching_precedent_file_names("asker_is_landlord")
asker_tenant = get_matching_precedent_file_names("asker_is_tenant")
ask_lease_modification = get_ask_lease_modification()
ask_retake_rental = get_matching_precedent_file_names("landlord_demand_retake_apartment")
ask_lower_rent = get_matching_precedent_file_names("tenant_demand_rent_decrease")
ask_damages = get_matching_precedent_file_names("landlord_demand_damage")
ask_fixation_of_rent = get_matching_precedent_file_names("landlord_fix_rent")
asking_rent_payment = get_matching_precedent_file_names("landlord_money_cover_rent")
ask_access_rental = get_matching_precedent_file_names("landlord_demand_access_rental")

ask_resiliation = get_matching_precedent_file_names("demand_resiliation")
tenant_left = get_matching_precedent_file_names("tenant_left_without_paying")
late_payment = get_matching_precedent_file_names("tenant_continuous_late_payment")
menacing = get_matching_precedent_file_names("violent")
three_weeks_late = get_matching_precedent_file_names("three_weeks_late")
proof_of_late = get_matching_precedent_file_names("proof_of_late")
increased_rent = get_matching_precedent_file_names("rent_increased")
not_three_weeks_late = get_not_three_weeks_late()
lack_of_proof = get_matching_precedent_file_names("tenant_lacks_proof")
serious_prejudice = get_matching_precedent_file_names("landlord_serious_prejudice")
money_owed = get_matching_precedent_file_names("tenant_owes_rent")
no_rent_owed = get_matching_precedent_file_names("no_rent_owed")
proof_of_revenu = get_matching_precedent_file_names("proof_of_revenu")
bothers_others = get_matching_precedent_file_names("bothers_others")
non_respect_of_judgement = get_matching_precedent_file_names("disrespect_previous_judgement")
tenant_died = get_matching_precedent_file_names("tenant_dead")
tenant_damaged_rental = get_matching_precedent_file_names("tenant_damaged_rental")
tenant_negligence = get_matching_precedent_file_names("tenant_negligence")
tenant_is_bothered = get_matching_precedent_file_names("tenant_is_bothered")
is_not_habitable = get_matching_precedent_file_names("apartment_impropre")

bad_mutual_agreement = get_matching_precedent_file_names("tenant_landlord_agreement")
bad_paid_before_audience = get_matching_precedent_file_names("tenant_rent_paid_before_hearing")
bad_absent = get_matching_precedent_file_names("absent")
bad_incorrect_facts = get_matching_precedent_file_names("incorrect_facts")

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
