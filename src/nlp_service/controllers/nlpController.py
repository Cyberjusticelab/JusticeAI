from flask import jsonify, abort, make_response

from nlp_service.rasa.intent_threshold import IntentThreshold
from nlp_service.services import factService
from postgresql_db.models import *
from rasa.rasa_classifier import RasaClassifier
from services import mlService
from services.responseStrings import Responses

from nlp_service.app import db

from postgresql_db.models import Conversation, ClaimCategory, Fact

from outlier.outlier_detection import OutlierDetection

# Logging
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

# Rasa Classifier - RasaClassifier used for claim category determination and fact value classification.
rasaClassifier = RasaClassifier()
rasaClassifier.train(force_train=False)

# Intent Threshold - Used to determine whether or not Rasa classification was sufficient to determine intent
intentThreshold = IntentThreshold(min_percent_difference=0.3, min_confidence_threshold=0.3)

# Outlier detector - Predicts if the new message is a clear outlier based on a model trained with fact messages
outlier_detector = OutlierDetection()

"""
Classifies the claim category from the user's message, set the Conversation's claim cateogry, and returns the first question to ask.
conversation_id: ID of the Conversation
message: message from the user
:return JSON containing the next message the user should be given
"""


def classify_claim_category(conversation_id, message):
    if conversation_id is None or message is None:
        abort(make_response(jsonify(message="Must provide conversation_id and message"), 400))

    # Retrieve conversation
    conversation = db.session.query(Conversation).get(conversation_id)

    # Classify claim category based on message
    claim_category = __classify_claim_category(message)

    # Define the message that will be returned
    response = None

    if claim_category in Responses.static_claim_responses.keys():
        response = Responses.chooseFrom(Responses.static_claim_responses[claim_category])

    elif claim_category:
        # Set conversation's claim category
        conversation.claim_category = {
            'ask_lease_termination': ClaimCategory.LEASE_TERMINATION,
            'ask_rent_change': ClaimCategory.RENT_CHANGE,
            'ask_nonpayment': ClaimCategory.NONPAYMENT
        }[claim_category]

        # Get first fact based on claim category
        first_fact = factService.submit_claim_category(conversation.claim_category)
        first_fact_id = first_fact['fact_id']

        if first_fact_id:
            # Retrieve the Fact from DB
            first_fact = db.session.query(Fact).get(first_fact_id)

            # Save first fact as current fact
            conversation.current_fact = first_fact

            # Commit
            db.session.commit()

            # Generate next message
            first_fact_question = Responses.fact_question(first_fact.name)
            response = Responses.chooseFrom(Responses.category_acknowledge).format(
                claim_category=conversation.claim_category.value.lower().replace("_", " "),
                first_question=first_fact_question)
        else:
            response = Responses.chooseFrom(Responses.category_acknowledge).format(
                claim_category=conversation.claim_category.value.lower().replace("_", " "),
                first_question=Responses.chooseFrom(Responses.unimplemented_category_error))
    else:
        response = Responses.chooseFrom(Responses.clarify).format(previous_question="")

    return jsonify({
        "message": response
    })


"""
Classifies the value of the Conversation's current fact, based on the user's message.
conversation_id: ID of the conversation
message: message from the user
:return JSON containing the next message the user should be given
"""


def classify_fact_value(conversation_id, message):
    if conversation_id is None or message is None:
        abort(make_response(jsonify(message="Must provide conversation_id and message"), 400))

    # Retrieve conversation
    conversation = db.session.query(Conversation).get(conversation_id)

    # Retrieve current_fact from conversation
    current_fact = conversation.current_fact

    # Extract entity from message based on current fact
    question = None

    fact_entity_value = __extract_entity(current_fact.name, message)
    if fact_entity_value is not None:
        # Pass fact with extracted entity to ML service
        next_fact = factService.submit_resolved_fact(conversation, current_fact, fact_entity_value)
        new_fact_id = next_fact['fact_id']

        # Retrieve the Fact from DB
        if new_fact_id:
            new_fact = db.session.query(Fact).get(new_fact_id)

            # Set current_fact to new_fact (returned from ML service)
            conversation.current_fact = new_fact

            # Generate question for next fact (returned from ML service)
            question = Responses.fact_question(new_fact.name)
        else:
            # All facts have been resolved, submit request to ML service for prediction
            ml_prediction = mlService.submit_resolved_fact_list(conversation)

            prediction = mlService.extract_prediction(claim_category=conversation.claim_category.value,
                                                      ml_response=ml_prediction)

            # Generate statement for prediction
            question = Responses.prediction_statement(conversation.claim_category.value, prediction)

            # Append a fact dump for good measure
            question += "\nFACT DUMP: "
            for fact_entity in conversation.fact_entities:
                question += "{}:{}, ".format(fact_entity.fact.name, fact_entity.value)
    else:
        question = Responses.chooseFrom(Responses.clarify).format(
            previous_question=Responses.fact_question(current_fact.name))

    # Commit
    db.session.commit()

    return jsonify({
        "message": question
    })


"""
Classifies the claim category based on a message.
message: message from user
:returns problem category key
"""


def __classify_claim_category(message):
    classify_dict = rasaClassifier.classify_problem_category(message)
    log.debug("\nClassify Claim Category\n\tMessage: {}\n\tDict: {}".format(message, classify_dict))

    # Return the claim category, or None if the answer was insufficient in determining one
    if intentThreshold.is_sufficient(classify_dict):
        determined_claim_category = classify_dict['intent']
        return determined_claim_category['name']
    else:
        return None


"""
Extracts the value of a fact, based on the current fact
current_fact_name: which fact we are checking for i.e. is_student
message: the message given by the user
:returns the determined value for the fact specified
"""


def __extract_entity(current_fact_name, message):
    # First pass: outlier detection
    # TODO: For now, this is disabled while we are gathering data from beta users
    if 'OUTLIER_DETECTION' in os.environ:
        result = outlier_detector.predict_if_outlier([message.lower()])
        if result[0] == -1:
            return None

    classify_dict = rasaClassifier.classify_fact(current_fact_name, message)
    log.debug("\nClassify Fact\n\tMessage: {}\n\tDict: {}".format(message, classify_dict))

    # Return the fact value, or None if the answer was insufficient in determining one
    if intentThreshold.is_sufficient(classify_dict):
        determined_intent = classify_dict['intent']
        return determined_intent['name']
    else:
        return None
