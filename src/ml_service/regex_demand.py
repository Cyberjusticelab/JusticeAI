import os
import joblib
from feature_extraction.regex.regex_lib import RegexLib

regex_lib = RegexLib()


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
landlord_demand_lease_modification = get_matching_precedent_file_names("landlord_demand_lease_modification")
landlord_demand_retake_apartment = get_matching_precedent_file_names("landlord_demand_retake_apartment")
tenant_demand_rent_decrease = get_matching_precedent_file_names("tenant_demand_rent_decrease")
landlord_demand_damage = get_matching_precedent_file_names("landlord_demand_damage")
landlord_fix_rent = get_matching_precedent_file_names("landlord_fix_rent")
landlord_money_cover_rent = get_matching_precedent_file_names("landlord_money_cover_rent")
landlord_demand_access_rental = get_matching_precedent_file_names("landlord_demand_access_rental")

demand_resiliation = get_matching_precedent_file_names("demand_resiliation")
tenant_left_without_paying = get_matching_precedent_file_names("tenant_left_without_paying")
tenant_continuous_late_payment = get_matching_precedent_file_names("tenant_continuous_late_payment")
violent = get_matching_precedent_file_names("violent")
tenant_rent_not_paid_exactly_3_weeks = get_matching_precedent_file_names("tenant_rent_not_paid_exactly_3_weeks")
rent_increased = get_matching_precedent_file_names("rent_increased")
tenant_rent_late_less_than_3_weeks = get_matching_precedent_file_names("tenant_rent_late_less_than_3_weeks")
tenant_lacks_proof = get_matching_precedent_file_names("tenant_lacks_proof")
landlord_serious_prejudice = get_matching_precedent_file_names("landlord_serious_prejudice")
tenant_owes_rent = get_matching_precedent_file_names("tenant_owes_rent")
tenant_do_not_owe_rent = get_matching_precedent_file_names("tenant_do_not_owe_rent")
proof_of_revenu = get_matching_precedent_file_names("proof_of_revenu")
bothers_others = get_matching_precedent_file_names("bothers_others")
disrespect_previous_judgement = get_matching_precedent_file_names("disrespect_previous_judgement")
tenant_dead = get_matching_precedent_file_names("tenant_dead")
tenant_damaged_rental = get_matching_precedent_file_names("tenant_damaged_rental")
tenant_negligence = get_matching_precedent_file_names("tenant_negligence")
tenant_is_bothered = get_matching_precedent_file_names("tenant_is_bothered")
apartment_impropre = get_matching_precedent_file_names("apartment_impropre")

bad_tenant_landlord_agreement = get_matching_precedent_file_names("tenant_landlord_agreement")
bad_tenant_rent_paid_before_hearing = get_matching_precedent_file_names("tenant_rent_paid_before_hearing")
bad_absent = get_matching_precedent_file_names("absent")
bad_tenant_incorrect_facts = get_matching_precedent_file_names("tenant_incorrect_facts")

meta = tenant_owes_rent.union(
    tenant_left_without_paying).union(
    apartment_impropre).union(
    proof_of_revenu).union(
    tenant_continuous_late_payment).union(
    tenant_negligence).union(
    violent).union(
    tenant_rent_not_paid_exactly_3_weeks).union(
    tenant_is_bothered).union(
    rent_increased).union(
    tenant_rent_late_less_than_3_weeks).union(
    tenant_lacks_proof).union(
    landlord_serious_prejudice).union(
    tenant_damaged_rental).union(
    tenant_dead).union(
    tenant_do_not_owe_rent).union(
    disrespect_previous_judgement).union(
    bothers_others)

rem = demand_resiliation - bad_tenant_landlord_agreement - \
      bad_tenant_rent_paid_before_hearing - bad_absent - bad_tenant_incorrect_facts
inter = rem - meta.intersection(demand_resiliation)


all_precedents = set(os.listdir('precedents/text_bk'))
bad_precedents = bad_tenant_landlord_agreement.union(
    bad_tenant_rent_paid_before_hearing).union(bad_absent).union(bad_tenant_incorrect_facts)
good_precedents = all_precedents - bad_precedents
precedent_vector = dict((el, {}) for el in good_precedents)


fill_dict(precedent_vector, lease, 'lease')
fill_dict(precedent_vector, asker_landlord, 'asker_landlord')
fill_dict(precedent_vector, asker_tenant, 'asker_tenant')
fill_dict(precedent_vector, landlord_demand_lease_modification, 'landlord_demand_lease_modification')
fill_dict(precedent_vector, landlord_demand_retake_apartment, 'landlord_demand_retake_apartment')
fill_dict(precedent_vector, tenant_demand_rent_decrease, 'tenant_demand_rent_decrease')
fill_dict(precedent_vector, landlord_demand_damage, 'landlord_demand_damage')
fill_dict(precedent_vector, landlord_fix_rent, 'landlord_fix_rent')
fill_dict(precedent_vector, landlord_money_cover_rent, 'landlord_money_cover_rent')
fill_dict(precedent_vector, landlord_demand_access_rental, 'landlord_demand_access_rental')
fill_dict(precedent_vector, demand_resiliation, 'demand_resiliation')
fill_dict(precedent_vector, tenant_left_without_paying, 'tenant_left_without_paying')
fill_dict(precedent_vector, tenant_continuous_late_payment, 'tenant_continuous_late_payment')
fill_dict(precedent_vector, violent, 'violent')
fill_dict(precedent_vector, tenant_rent_not_paid_exactly_3_weeks, 'tenant_rent_not_paid_exactly_3_weeks')
fill_dict(precedent_vector, rent_increased, 'rent_increased')
fill_dict(precedent_vector, tenant_rent_late_less_than_3_weeks, 'tenant_rent_late_less_than_3_weeks')
fill_dict(precedent_vector, tenant_lacks_proof, 'tenant_lacks_proof')
fill_dict(precedent_vector, landlord_serious_prejudice, 'landlord_serious_prejudice')
fill_dict(precedent_vector, tenant_owes_rent, 'tenant_owes_rent')
fill_dict(precedent_vector, tenant_do_not_owe_rent, 'tenant_do_not_owe_rent')
fill_dict(precedent_vector, proof_of_revenu, 'proof_of_revenu')
fill_dict(precedent_vector, bothers_others, 'bothers_others')
fill_dict(precedent_vector, disrespect_previous_judgement, 'disrespect_previous_judgement')
fill_dict(precedent_vector, tenant_dead, 'tenant_died')
fill_dict(precedent_vector, tenant_damaged_rental, 'tenant_damaged_rental')
fill_dict(precedent_vector, tenant_negligence, 'tenant_negligence')
fill_dict(precedent_vector, tenant_is_bothered, 'tenant_is_bothered')
fill_dict(precedent_vector, apartment_impropre, 'apartment_impropre')

joblib.dump(precedent_vector, 'prec.bin')

print("diff total:")
print(len(inter))

print("diff %:")
print(len(inter) * 100.0 / len(rem))

with open('diff.txt', 'w') as file:
    for item in inter:
        file.write("%s\n" % item)
