import requests

from postgresql_db.models import Fact, FactEntity, PersonType

ML_URL = "http://ml_service:3001"

"""
Submits list of resolved facts to ML endpoint. Only done once all
facts have been asked and resolved.
Returns the first fact to ask a question for, based on claim category.
conversation: the current conversation
:returns Outcomes vector with true/false, depending on chance of winning case
"""


def submit_resolved_fact_list(conversation):
    req_dict = {
        "demands": generate_demand_dict(),
        "facts": generate_fact_dict(conversation)
    }
    res = requests.post("{}/{}".format(ML_URL, "predict"), json=req_dict)
    return res.json()


"""
Given a claim cateogry and the ml service response, will extract the prediction 
performing any necessary mappings.
claim_category: the current conversation's claim category as a string
ml_response: the response dict received from ml service
:returns Outcomes vector with true/false, depending on chance of winning case
"""


def extract_prediction(claim_category, ml_response):
    outcome_mapping = {
        "lease_termination": "lease_resiliation"
    }

    outcome_key = None
    if claim_category in outcome_mapping:
        outcome_key = outcome_mapping[claim_category.lower()]

    if outcome_key:
        return True if ml_response[outcome_key] == 1 else False

    return False


"""
Generates demand dictionary with default values for ML service input
:returns Demand dictionary with default values
"""


def generate_demand_dict():
    demand_dict = {
        "demand_lease_modification": 0,
        "demand_resiliation": 1,
        "landlord_claim_interest_damage": 0,
        "landlord_demand_access_rental": 0,
        "landlord_demand_bank_fee": 0,
        "landlord_demand_damage": 0,
        "landlord_demand_legal_fees": 0,
        "landlord_demand_retake_apartment": 0,
        "landlord_demand_utility_fee": 0,
        "landlord_fix_rent": 0,
        "landlord_lease_termination": 0,
        "landlord_money_cover_rent": 0,
        "paid_judicial_fees": 0,
        "tenant_claims_harassment": 0,
        "tenant_cover_rent": 0,
        "tenant_demands_decision_retraction": 0,
        "tenant_demand_indemnity_Code_Civil": 0,
        "tenant_demand_indemnity_damage": 0,
        "tenant_demand_indemnity_judicial_fee": 0,
        "tenant_demand_interest_damage": 0,
        "tenant_demands_money": 0,
        "tenant_demand_rent_decrease": 0,
        "tenant_respect_of_contract": 0,
        "tenant_eviction": 0
    }
    return demand_dict


"""
Generates fact dictionary for ML service. Maps values for unasked facts
based on asked facts, or provides default mappings.
:returns Fact dictionary with mapped facts and resolved facts
"""

all_ml_facts = [
    "absent",
    "apartment_impropre",
    "apartment_infestation",
    "asker_is_landlord",
    "asker_is_tenant",
    "bothers_others",
    "disrespect_previous_judgement",
    "incorrect_facts",
    "landlord_inspector_fees",
    "landlord_notifies_tenant_retake_apartment",
    "landlord_pays_indemnity",
    "landlord_prejudice_justified",
    "landlord_relocation_indemnity_fees",
    "landlord_rent_change",
    "landlord_rent_change_doc_renseignements",
    "landlord_rent_change_piece_justification",
    "landlord_rent_change_receipts",
    "landlord_retakes_apartment",
    "landlord_retakes_apartment_indemnity",
    "landlord_sends_demand_regie_logement",
    "landlord_serious_prejudice",
    "lease",
    "proof_of_late",
    "proof_of_revenu",
    "rent_increased",
    "tenant_bad_payment_habits",
    "tenant_continuous_late_payment",
    "tenant_damaged_rental",
    "tenant_dead",
    "tenant_declare_insalubre",
    "tenant_financial_problem",
    "tenant_group_responsability",
    "tenant_individual_responsability",
    "tenant_is_bothered",
    "lack_of_proof",
    "tenant_landlord_agreement",
    "tenant_lease_fixed",
    "tenant_lease_indeterminate",
    "tenant_left_without_paying",
    "tenant_monthly_payment",
    "tenant_negligence",
    "tenant_not_request_cancel_lease",
    "tenant_owes_rent",
    "tenant_refuses_retake_apartment",
    "tenant_rent_not_paid_less_3_weeks",
    "tenant_rent_not_paid_more_3_weeks",
    "tenant_rent_paid_before_hearing",
    "tenant_violence",
    "tenant_withold_rent_without_permission",
    "violent"
]


def generate_fact_dict(conversation):
    resolved_facts = {}

    # Initialize expected facts with all false
    for expected_fact in all_ml_facts:
        resolved_facts[expected_fact] = False

    # Add all resolved facts
    for fact_entity in conversation.fact_entities:
        fact_entity_name = fact_entity.fact.name
        if fact_entity.value == "true":
            resolved_facts[fact_entity_name] = True
        elif fact_entity.value == "false":
            resolved_facts[fact_entity_name] = False

    ############
    # Mappings #
    ############

    # Perform asker mapping
    if conversation.person_type is PersonType.LANDLORD:
        resolved_facts['asker_is_landlord'] = True
        resolved_facts['asker_is_tenant'] = False
    else:
        resolved_facts['asker_is_landlord'] = False
        resolved_facts['asker_is_tenant'] = True

    # Perform one to one mappings
    resolved_facts['violent'] = resolved_facts['tenant_violence']

    resolved_facts['landlord_rent_change_piece_justification'] = resolved_facts[
        'landlord_rent_change_doc_renseignements']
    resolved_facts['landlord_rent_change_receipts'] = resolved_facts[
        'landlord_rent_change_doc_renseignements']

    # Perform mappings with dependencies
    resolved_facts['tenant_lease_indeterminate'] = not resolved_facts['tenant_lease_fixed']
    resolved_facts['lease'] = resolved_facts['tenant_lease_fixed']
    resolved_facts['tenant_rent_not_paid_less_3_weeks'] = not resolved_facts['tenant_rent_not_paid_more_3_weeks']

    # Convert true and false to 1 and 0
    for fact_entity in resolved_facts:
        if resolved_facts[fact_entity]:
            resolved_facts[fact_entity] = 1
        else:
            resolved_facts[fact_entity] = 0

    return resolved_facts
