from flask import jsonify, abort, make_response

# from postgresql_db.models import *
from rasa.rasa_classifier import RasaClassifier
from services import mlService
from services.responseStrings import Responses

# Globals
from src.postgresql_db.models import Conversation, ClaimCategory

minimum_percent_difference = 0.3

# Rasa Classifier
rasaClassifier = RasaClassifier()
rasaClassifier.train(force_train=True)


def classify_claim_category(conversation_id, message):
    if conversation_id is None or message is None:
        abort(make_response(jsonify(message="Must provide conversation_id and message"), 400))

    # Retrieve conversation
    conversation = Conversation.query.get(conversation_id)

    # Classify claim category based on message
    claim_category = __classify_claim_category(message)

    # Set conversation's claim category
    conversation.claim_category = {
        'ask_lease_termination': ClaimCategory.LEASE_TERMINATION,
        'ask_rent_change': ClaimCategory.RENT_CHANGE,
        'ask_nonpayment': ClaimCategory.NONPAYMENT,
        'ask_deposits': ClaimCategory.DEPOSITS
    }[claim_category]

    # Get first fact based on claim category
    first_fact = mlService.submit_claim_category(conversation_id, claim_category)

    # Save first fact as current fact
    conversation.current_fact = first_fact

    # Generate next message
    first_fact_question = Responses.fact_question(first_fact)
    message = Responses.chooseFrom(Responses.category_acknowledge).format(claim_category=claim_category,
                                                                          first_question=first_fact_question)

    return jsonify({
        "message": message
    })


def classify_fact_value(conversation_id, message):
    if conversation_id is None or message is None:
        abort(make_response(jsonify(message="Must provide conversation_id and message"), 400))

    # Retrieve conversation
    conversation = Conversation.query.get(conversation_id)

    # Retrieve current_fact from conversation
    current_fact = conversation.current_fact

    # Extract entity from message based on current fact
    question = None

    fact_entity_value = __extract_entity(current_fact, message)
    if fact_entity_value is not None:
        # Pass fact with extracted entity to ML service
        new_fact = mlService.submit_resolved_fact(conversation_id, current_fact, fact_entity_value)

        # Set current_fact to new_fact (returned from ML service)
        conversation.current_fact = new_fact
        # db.session.commit()

        # Generate question for next fact (returned from ML service)
        question = Responses.fact_question(new_fact)
    else:
        question = Responses.chooseFrom(Responses.clarify)

    return jsonify({
        "message": question
    })


def __classify_claim_category(message):
    classify_dict = rasaClassifier.classify_problem_category(message)

    # Return the claim category, or None if the answer was insufficient in determining one
    if __is_answer_sufficient(classify_dict):
        determined_problem_category = classify_dict['intent']
        print("Confidence: {}%".format(round(determined_problem_category['confidence'], 3) * 100))
        print("Intent: {}".format(determined_problem_category['name']))
        return determined_problem_category['name']
    else:
        return None


def __extract_entity(current_fact, message):
    classify_dict = rasaClassifier.classify_fact(current_fact, message)
    print(classify_dict)

    # Return the fact value, or None if the answer was insufficient in determining one
    if __is_answer_sufficient(classify_dict):
        determined_intent = classify_dict['intent']
        print("Confidence: {}%".format(round(determined_intent['confidence'], 3) * 100))
        print("Intent: {}".format(determined_intent['name']))
        return determined_intent['name']
    else:
        return None


# Determine confidence of returned intent
def __is_answer_sufficient(classify_dict):
    if len(classify_dict['intent_ranking']) > 1:
        percent_difference = RasaClassifier.intent_percent_difference(classify_dict)
        print("Percent Difference: {}%".format(round(percent_difference, 3) * 100))
        if percent_difference < minimum_percent_difference:
            return False
    return True
