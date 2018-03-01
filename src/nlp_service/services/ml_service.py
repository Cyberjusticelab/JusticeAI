import requests

from postgresql_db.models import PersonType, FactType

# Logging
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

# ML Api Url
ML_URL = "http://ml_service:3001"

# Dict containing outcome fact mappings
outcome_facts = {}

# Dict containing antifact mappings
anti_facts = {}


def get_outcome_facts():
    """
    :return: Dict of outcomes with relevant facts from the ML endpoint
    """
    global outcome_facts
    if not outcome_facts:
        outcome_facts = requests.get("{}/{}".format(ML_URL, "weights")).json()

    return outcome_facts


def get_anti_facts():
    """
    :return: Dict of antifacts from the ML endpoint.
    """
    global anti_facts
    if not anti_facts:
        anti_facts = requests.get("{}/{}".format(ML_URL, "antifacts")).json()

    return anti_facts


def submit_resolved_fact_list(conversation):
    """
    Submits list of resolved facts to ML endpoint.
    Should only be done once all facts have been asked and resolved.
    :param conversation: The current conversation
    :return: Outcomes vector from ML service
    """

    fact_dict = generate_fact_dict(conversation)
    log.debug("Submitting Resolved Fact Dict\n\tFact Dict: {}".format(fact_dict))

    req_dict = {
        "facts": fact_dict
    }
    res = requests.post("{}/{}".format(ML_URL, "predict"), json=req_dict)
    return res.json()


def extract_prediction(claim_category, ml_response):
    """
    Given a claim category and the ml service response, will extract the prediction performing any necessary mappings.
    :param claim_category: The current conversation's claim category as a string
    :param ml_response: The response dict received from ml service
    :return: Dict of relevant outcomes for the claim category returned by ML service
    """

    relevant_outcomes = {
        "lease_termination": ['orders_resiliation'],
        "nonpayment": ['tenant_ordered_to_pay_landlord',
                       'tenant_ordered_to_pay_landlord_legal_fees',
                       'additional_indemnity_money']
    }

    claim_category = claim_category.lower()
    outcome_list = []

    if claim_category in relevant_outcomes:
        outcome_list = relevant_outcomes[claim_category]

    resolved_outcomes = {}
    if len(outcome_list) > 0:
        for outcome in outcome_list:
            resolved_outcomes[outcome] = ml_response['outcomes_vector'][outcome]

    return resolved_outcomes


def generate_fact_dict(conversation):
    """
    Generates fact dictionary for ML service.
    Maps values for unasked facts based on asked facts, or provides default mappings.
    :param conversation: The current conversation
    :return: Fact dictionary with mapped facts and resolved facts
    """

    resolved_facts = {}

    # Add all resolved facts
    for fact_entity in conversation.fact_entities:
        fact_entity_name = fact_entity.fact.name
        fact_entity_type = fact_entity.fact.type

        if fact_entity_type == FactType.BOOLEAN:
            if fact_entity.value == "true":
                resolved_facts[fact_entity_name] = True
            elif fact_entity.value == "false":
                resolved_facts[fact_entity_name] = False
        elif fact_entity_type == FactType.MONEY:
            resolved_facts[fact_entity_name] = float(fact_entity.value)

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

    # Perform anti-fact mappings
    anti_facts = get_anti_facts()
    for fact in list(resolved_facts):  # This is done because a dict cannot be changed while iterating through it
        if fact in anti_facts.keys():
            anti_fact_key_name = anti_facts[fact]
            resolved_facts[anti_fact_key_name] = not resolved_facts[fact]
        elif fact in anti_facts.values():
            anti_fact_key_name = [k for k, v in anti_facts.items() if v == fact][0]
            resolved_facts[anti_fact_key_name] = not resolved_facts[fact]

    # Convert true and false to 1 and 0
    for fact_entity in resolved_facts:
        if resolved_facts[fact_entity] is True:
            resolved_facts[fact_entity] = 1
        elif resolved_facts[fact_entity] is False:
            resolved_facts[fact_entity] = 0

    return resolved_facts
