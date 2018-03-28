from collections import OrderedDict
from datetime import timedelta

from nlp_service.services import ml_service
from nlp_service.services.response_strings import Responses
from postgresql_db.models import FactEntity, Fact, FactType


def get_resolved_fact_keys(conversation):
    """
    Returns a list of all the resolved facts for a conversation as string keys
    :param conversation: The current conversation
    :return: List of all resolved fact names as strings
    """
    return [fact_entity_row.fact.name for fact_entity_row in conversation.fact_entities]


def submit_claim_category(conversation):
    """
    Returns the first fact after submitting a determined claim category
    :param conversation: The current conversation
    :return: First fact id to ask a question for
    """

    return {
        'fact_id': get_next_fact(conversation)
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

    return {
        'fact_id': get_next_fact(conversation)
    }


# Dictionary that maps claim categories to outcomes. Facts from these outcomes will be used to
# ask questions to users for a particular claim category
outcome_mapping = {
    "lease_termination": [
        "orders_resiliation"
    ],
    "nonpayment": [
        "tenant_ordered_to_pay_landlord",
        "tenant_ordered_to_pay_landlord_legal_fees",
        "additional_indemnity_money"
    ],
    "retake_rental": [
        "authorize_landlord_retake_apartment"
    ]
}


def get_category_fact_list(claim_category):
    """
    Returns a dict containing a list fo important facts "facts", and non-important facts "additional_facts" for a claim category
    :param claim_category: Claim category as a string
    """
    category_fact_dict = {
        "facts": [],
        "additional_facts": []
    }
    all_category_outcomes = outcome_mapping[claim_category.lower()]

    # Filter out only facts relevant to those defined in outcome_mapping for each outcome
    outcome_facts = ml_service.get_outcome_facts()
    for outcome in outcome_facts:
        if outcome in all_category_outcomes:
            category_fact_dict["facts"].extend(outcome_facts[outcome]["important_facts"])
            category_fact_dict["additional_facts"].extend(outcome_facts[outcome]["additional_facts"])

    # Replace anti facts with askable facts, if applicable
    anti_facts = ml_service.get_anti_facts()
    category_fact_dict["facts"] = replace_anti_facts(category_fact_dict["facts"], anti_facts)
    category_fact_dict["additional_facts"] = replace_anti_facts(category_fact_dict["additional_facts"], anti_facts)

    # Remove any additional facts that are important facts
    category_fact_dict["additional_facts"] = [fact for fact in category_fact_dict["additional_facts"] if
                                              fact not in category_fact_dict["facts"]]

    # Remove Duplicates while maintaining order
    category_fact_dict["facts"] = list(OrderedDict.fromkeys(category_fact_dict["facts"]))
    category_fact_dict["additional_facts"] = list(OrderedDict.fromkeys(category_fact_dict["additional_facts"]))

    # Filter out unaskable facts
    askable_facts = Responses.fact_questions.keys()
    category_fact_dict["facts"] = [fact for fact in category_fact_dict["facts"] if fact in askable_facts]
    category_fact_dict["additional_facts"] = [fact for fact in category_fact_dict["additional_facts"] if
                                              fact in askable_facts]

    return category_fact_dict


def replace_anti_facts(fact_list, anti_fact_dict):
    """
    Since anti-facts are returned in a dict, either the key or the value is the askable fact. This function replaces
    all unaskable facts with ones that can have questions asked for them
    :param fact_list: A list of facts
    :param anti_fact_dict: A dict of fact:anti-fact, anti-fact:fact pairs
    :return: List of facts that can be asked, and not their mappable antifact
    """

    filtered_fact_list = []
    askable_facts = Responses.fact_questions.keys()
    for fact in fact_list:
        if fact not in askable_facts:
            if fact in anti_fact_dict.keys():
                filtered_fact_list.append(anti_fact_dict[fact])
            elif fact in anti_fact_dict.values():
                fact_key_value = [k for k, v in anti_fact_dict.items() if v == fact][0]
                filtered_fact_list.append(fact_key_value)
        else:
            filtered_fact_list.append(fact)

    return filtered_fact_list


def get_next_fact(conversation):
    """
    Returns next fact id based on claim category given the resolved facts.
    :param conversation: The current conversation
    :return: Next fact id to ask a question for
    """

    all_category_facts = get_category_fact_list(conversation.claim_category.value)
    facts_resolved = get_resolved_fact_keys(conversation)
    facts_unresolved = []

    if has_important_facts(conversation):
        facts_unresolved = [fact for fact in all_category_facts["facts"] if fact not in facts_resolved]
    elif has_additional_facts(conversation):
        facts_unresolved = [fact for fact in all_category_facts["additional_facts"] if fact not in facts_resolved]

    # Pick the first unresolved fact, return None if none remain
    if len(facts_unresolved) == 0:
        return None

    fact_name = facts_unresolved[0]
    fact = Fact.query.filter_by(name=fact_name).first()
    return fact.id


def has_important_facts(conversation):
    """
    :param conversation: The current conversation
    :return: True if important facts still exist for this conversation
    """

    all_category_facts = get_category_fact_list(conversation.claim_category.value)
    facts_resolved = get_resolved_fact_keys(conversation)
    facts_unresolved = [fact for fact in all_category_facts["facts"] if fact not in facts_resolved]

    if len(facts_unresolved) == 0:
        return False
    return True


def has_additional_facts(conversation):
    """
    :param conversation: The current conversation
    :return: True if additional facts still exist for this conversation
    """

    all_category_facts = get_category_fact_list(conversation.claim_category.value)
    facts_resolved = get_resolved_fact_keys(conversation)
    facts_unresolved = [fact for fact in all_category_facts["additional_facts"] if fact not in facts_resolved]

    if len(facts_unresolved) == 0:
        return False
    return True


def count_important_facts_resolved(conversation):
    """
    :param conversation: The current conversation
    :return: Returns the count of how many additional facts have been resolved
    """

    all_category_facts = get_category_fact_list(conversation.claim_category.value)
    facts_resolved = get_resolved_fact_keys(conversation)
    important_facts_resolved = [fact for fact in all_category_facts["facts"] if fact in facts_resolved]
    return len(important_facts_resolved)


def count_additional_facts_resolved(conversation):
    """
    :param conversation: The current conversation
    :return: Returns the count of how many additional facts have been resolved
    """

    all_category_facts = get_category_fact_list(conversation.claim_category.value)
    facts_resolved = get_resolved_fact_keys(conversation)
    additional_facts_resolved = [fact for fact in all_category_facts["additional_facts"] if fact in facts_resolved]
    return len(additional_facts_resolved)


def count_additional_facts_unresolved(conversation):
    """
    :param conversation: The current conversation
    :return: Returns the count of how many additional facts have not been resolved yet
    """

    all_category_facts = get_category_fact_list(conversation.claim_category.value)
    facts_resolved = get_resolved_fact_keys(conversation)
    additional_facts_unresolved = [fact for fact in all_category_facts["additional_facts"] if
                                   fact not in facts_resolved]
    return len(additional_facts_unresolved)


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
    elif fact_type == FactType.DURATION_MONTHS:
        if intent_name == 'true':
            for entity in entities:
                if entity['entity'] == 'duration':
                    return extract_month_from_duration(entity)
            return 0  # Default
        elif intent_name == 'false':
            return 0


def extract_month_from_duration(extracted_entity):
    """
    Takes a ner_duckling entity duration classification and converts it to a timespan representing months.
    Note that since an integer is returned, it will be rounded. Thus, expect behavior such as 6 weeks = 1 month.

    :param extracted_entity:
        A ner_duckling duration entity of this form. Will automatically coerce durations not classified
        as months, for example 'week' or 'day'.

        {
            'start': 0,
            'end': 8,
            'text': '15 weeks',
            'value': 15.0,
            'additional_info': {
                'value': 15.0,
                'unit': 'week',
                'year': None,
                'month': None,
                'day': None,
                'hour': None,
                'minute': None,
                'second': None,
                },
            'entity': 'duration',
            'extractor': 'ner_duckling',
        }

    :return: Integer representing number of months
    """

    if extracted_entity['additional_info']['month']:
        return extracted_entity['additional_info']['month']

    time_value = extracted_entity['additional_info']['value']
    time_unit = extracted_entity['additional_info']['unit']

    time_delta = {
        "year": timedelta(weeks=time_value * 52),
        "week": timedelta(weeks=time_value),
        "day": timedelta(days=time_value),
        "hour": timedelta(hours=time_value),
        "minute": timedelta(minutes=time_value),
        "second": timedelta(seconds=time_value),
    }[time_unit]

    return int(round(time_delta.days / 30))
