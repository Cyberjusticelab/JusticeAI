from nlp_service.services import ml_service
from postgresql_db.models import FactEntity, Fact, FactType


def submit_claim_category(claim_category):
    """
    Returns the first fact after submitting a determined claim category
    :param claim_category: The claim category determined from user input as a string
    :return: First fact id to ask a question for
    """

    return {
        'fact_id': get_next_fact(claim_category, [])
    }


def submit_resolved_fact(conversation, current_fact, entity_value):
    """
    After resolving a fact, returns the next fact to ask a question for
    :param conversation: The current conversation
    :param current_fact: The current fact
    :param entity_value: Classified value of the current fact
    :return: Next fact id to ask a question for
    """

    # Create new FactEntity and attach to conversation
    fact_entity = FactEntity(fact=current_fact, value=entity_value)
    conversation.fact_entities.append(fact_entity)

    # Get all resolved facts for Conversation
    facts_resolved = [fact_entity_row.fact.name for fact_entity_row in conversation.fact_entities]

    return {
        'fact_id': get_next_fact(conversation.claim_category, facts_resolved)
    }


# This can be replaced with a more dynamic solution using MLService to obtain fact lists
outcome_facts = {}
outcome_mapping = {
    "lease_termination": [
        "orders_resiliation"
    ],
    "nonpayment": [
        "tenant_ordered_to_pay_landlord",
        "tenant_ordered_to_pay_landlord_legal_fees",
        "additional_indemnity_money"
    ]
}


def get_outcome_facts():
    """
    Gets the outcome facts dict with data from ml service
    """

    global outcome_facts
    if not outcome_facts:
        outcome_facts = ml_service.get_outcome_facts()
    return outcome_facts


def get_category_fact_list(claim_category):
    """
    Returns a dict containing a list fo important facts "facts", and non-important facts "not_important_facts" for a claim category
    :param claim_category: Claim category as a string
    """
    category_fact_dict = {
        "facts": [],
        "not_important_facts": []
    }
    all_category_outcomes = outcome_mapping[claim_category.value.lower()]

    for outcome in get_outcome_facts():
        if outcome in all_category_outcomes:
            category_fact_dict["facts"].append(outcome["important_facts"])
            category_fact_dict["not_important_facts"].append(outcome["not_important_facts"])

    # Remove Duplicates
    category_fact_dict["facts"] = list(set(category_fact_dict["facts"]))
    category_fact_dict["not_important_facts"] = list(set(category_fact_dict["not_important_facts"]))

    return category_fact_dict


def get_next_fact(claim_category, facts_resolved):
    """
    Returns next fact id based on claim category given the resolved facts.
    :param claim_category: Claim category of the conversation as a string
    :param facts_resolved: List of all resolved fact keys for the conversation
    :return: Next fact id to ask a question for
    """

    all_category_facts = get_category_fact_list(claim_category)
    facts_unresolved = [fact for fact in all_category_facts["facts"] if fact not in facts_resolved]

    # Pick the first unresolved fact, return None if none remain
    if len(facts_unresolved) == 0:
        return None

    fact_name = facts_unresolved[0]
    fact = Fact.query.filter_by(name=fact_name).first()
    return fact.id


def extract_fact_by_type(fact_type, intent, entities):
    """
    Returns the relevant information for a particular FactType based on rasa nlu classification data.
    :param fact_type: The FactType of the relevant fact
    :param intent: The intent returned by RASA. Has 'name' and 'confidence' attributes.
    :param entities: A list of extracted entities. Can be empty.
    :return: Final fact value based on fact_type
    """

    intent_name = intent['name']

    if fact_type == FactType.BOOLEAN:
        return intent_name
    elif fact_type == FactType.MONEY:
        if intent_name == 'true':
            for entity in entities:
                if entity['entity'] == 'amount-of-money':
                    return entity['value']
        elif intent_name == 'false':
            return 0
