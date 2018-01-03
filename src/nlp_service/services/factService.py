from postgresql_db.models import FactEntity, Fact

"""
Simulates the return values of the proposed ML service.
Returns the first fact to ask a question for, based on claim category.
claim_category: The claim category determined from user input
:returns First fact to ask a question for
"""


def submit_claim_category(claim_category):
    return {
        'fact_id': get_next_fact(claim_category, [])
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
        'fact_id': get_next_fact(conversation.claim_category, facts_resolved)
    }


"""
Returns next fact based on claim category given the resolved facts. 
claim_category: claim category of the conversation
facts_resolved: list of resolved fact keys
:returns Next fact id to ask
"""

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
    "rent_change": [
        "apartment_impropre",
    ],
    "nonpayment": [
        "apartment_impropre",
    ],
    "deposits": [
        "apartment_impropre",
    ]
}


def get_next_fact(claim_category, facts_resolved):
    all_category_facts = fact_mapping[claim_category.value.lower()]
    facts_unresolved = [fact for fact in all_category_facts if fact not in facts_resolved]

    # Pick the first unresolved fact, return None if none remain
    if len(facts_unresolved) == 0:
        return None

    fact_name = facts_unresolved[0]
    fact = Fact.query.filter_by(name=fact_name).first()
    return fact.id
