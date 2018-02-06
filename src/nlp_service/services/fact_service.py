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
fact_mapping = {
    "lease_termination": [
        "tenant_rent_not_paid_more_3_weeks",
        "tenant_violence",
        "tenant_owes_rent",
        "tenant_monthly_payment",
        "landlord_retakes_apartment",
        "tenant_bad_payment_habits",
        "apartment_impropre",
        "landlord_rent_change",
        "tenant_left_without_paying",
    ],
    "nonpayment": [
        "tenant_owes_rent",
        "tenant_withold_rent_without_permission",
        "tenant_continuous_late_payment",
        "tenant_rent_not_paid_more_3_weeks",
        "tenant_rent_paid_before_hearing",
        "landlord_serious_prejudice"
    ]
}


def get_next_fact(claim_category, facts_resolved):
    """
    Returns next fact id based on claim category given the resolved facts.
    :param claim_category: Claim category of the conversation as a string
    :param facts_resolved: List of all resolved fact keys for the conversation
    :return: Next fact id to ask a question for
    """

    all_category_facts = fact_mapping[claim_category.value.lower()]
    facts_unresolved = [fact for fact in all_category_facts if fact not in facts_resolved]

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
