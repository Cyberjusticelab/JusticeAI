import requests

from postgresql_db.models import Fact, FactEntity, PersonType

ML_URL = "http://ml_service:3001"

"""
Simulates the return values of the proposed ML service.
Returns the first fact to ask a question for, based on claim category.
claim_category: The claim category determined from user input
:returns First fact to ask a question for
"""


def submit_claim_category(claim_category):
    return {
        'fact_id': dummy_next_fact(claim_category, [])
    }


"""
Simulates the return values of the proposed ML service.
Returns the next fact to ask a question for
conversation: the current conversation
current_fact: the current fact
entity_value: value of the fact
:returns Next fact to ask a question for
"""


def submit_resolved_fact(conversation, current_fact, entity_value):
    # Create new FactEntity and attach to conversation
    fact_entity = FactEntity(fact=current_fact, value=entity_value)
    conversation.fact_entities.append(fact_entity)

    # Get all resolved facts for Conversation
    facts_resolved = [fact_entity_row.fact.name for fact_entity_row in conversation.fact_entities]

    return {
        'fact_id': dummy_next_fact(conversation.claim_category, facts_resolved)
    }


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


def generate_fact_dict(conversation):
    resolved_facts = {}

    # Add all resolved facts
    for fact_entity in conversation.fact_entities:
        fact_entity_name = fact_entity.fact.name
        if fact_entity.value == "true":
            resolved_facts[fact_entity_name] = True
        elif fact_entity.value == "false":
            resolved_facts[fact_entity_name] = False

    # Perform asker mapping
    if conversation.person_type is PersonType.LANDLORD:
        resolved_facts['asker_is_landlord'] = True
        resolved_facts['asker_is_tenant'] = False
    else:
        resolved_facts['asker_is_landlord'] = False
        resolved_facts['asker_is_tenant'] = True

    # Perform mappings with defaults
    resolved_facts['absent'] = False
    resolved_facts['incorrect_facts'] = False
    resolved_facts['landlord_pays_indemnity'] = False
    resolved_facts['landlord_prejudice_justified'] = False
    resolved_facts['landlord_serious_prejudice'] = False
    resolved_facts['proof_of_late'] = False
    resolved_facts['tenant_is_bothered'] = False
    resolved_facts['lack_of_proof'] = False
    resolved_facts['tenant_rent_paid_before_hearing'] = False

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


"""
Dummy method that returns next fact given resolved facts. Stub implementation for
proposed ML service.
claim_category: claim category of the conversation
facts_resolved: list of resolved fact keys
:returns Next fact id to ask
"""


def dummy_next_fact(claim_category, facts_resolved):
    all_facts = [
        "apartment_impropre",
        "landlord_relocation_indemnity_fees",
        "landlord_rent_change",
        "landlord_retakes_apartment",
        "landlord_sends_demand_regie_logement",
        "tenant_lease_fixed",
        "tenant_bad_payment_habits",
        "tenant_continuous_late_payment",
        "tenant_individual_responsability",
        "tenant_left_without_paying",
        "tenant_monthly_payment",
        "tenant_owes_rent",
        "tenant_rent_not_paid_more_3_weeks",
        "tenant_violence",
    ]

    fact_dict = {
        "lease_termination": all_facts,
        "rent_change": all_facts,
        "nonpayment": all_facts,
        "deposits": all_facts
    }

    all_category_facts = fact_dict[claim_category.value.lower()]
    facts_unresolved = [fact for fact in all_category_facts if fact not in facts_resolved]

    # Pick the first unresolved fact, return None if none remain
    if len(facts_unresolved) == 0:
        return None

    fact_name = facts_unresolved[0]
    fact = Fact.query.filter_by(name=fact_name).first()
    return fact.id
