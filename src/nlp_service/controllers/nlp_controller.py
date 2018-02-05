from flask import jsonify, abort, make_response

from nlp_service.rasa.intent_threshold import IntentThreshold
from nlp_service.services import fact_service
from postgresql_db.models import *
from rasa.rasa_classifier import RasaClassifier
from services import ml_service
from services.response_strings import Responses

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
intentThreshold = IntentThreshold(min_percent_difference=0.0, min_confidence_threshold=0.15)

# Outlier detector - Predicts if the new message is a clear outlier based on a model trained with fact messages
outlier_detector = OutlierDetection()


def classify_claim_category(conversation_id, message):
    """
    Classifies the claim category from the user's message, set the Conversation's claim category
    and returns the first question to ask.
    :param conversation_id: ID of the Conversation
    :param message: Message from the user
    :return: JSON containing the next message the user should be given
    """

    if conversation_id is None or message is None:
        abort(make_response(jsonify(message="Must provide conversation_id and message"), 400))

    # Retrieve conversation
    conversation = db.session.query(Conversation).get(conversation_id)

    # Classify claim category based on message
    claim_category = __classify_claim_category(message=message, person_type=conversation.person_type.value)

    # Define the message that will be returned
    response = None

    if claim_category in Responses.static_claim_responses.keys():
        response = Responses.faq_statement(claim_category, conversation.person_type.value)

    elif claim_category:
        # Set conversation's claim category
        conversation.claim_category = {
            'ask_lease_termination': ClaimCategory.LEASE_TERMINATION,
            'ask_nonpayment': ClaimCategory.NONPAYMENT
        }[claim_category]

        # Get first fact based on claim category
        first_fact = fact_service.submit_claim_category(conversation.claim_category)
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


def classify_fact_value(conversation_id, message):
    """
    Classifies the value of the Conversation's current fact, based on the user's message.
    :param conversation_id: ID of the conversation
    :param message: Message from the user
    :return: JSON containing the next message the user should be given
    """

    if conversation_id is None or message is None:
        abort(make_response(jsonify(message="Must provide conversation_id and message"), 400))

    # Retrieve conversation
    conversation = db.session.query(Conversation).get(conversation_id)

    # Retrieve current_fact from conversation
    current_fact = conversation.current_fact

    # Extract entity from message based on current fact
    question = None

    fact_entity_value = __extract_entity(current_fact.name, current_fact.type, message)
    if fact_entity_value is not None:
        # Pass fact with extracted entity to ML service
        next_fact = fact_service.submit_resolved_fact(conversation, current_fact, fact_entity_value)
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
            ml_prediction = ml_service.submit_resolved_fact_list(conversation)

            prediction_dict = ml_service.extract_prediction(claim_category=conversation.claim_category.value,
                                                            ml_response=ml_prediction)

            # Generate statement for prediction
            question = Responses.prediction_statement(conversation.claim_category.value, prediction_dict)
    else:
        question = Responses.chooseFrom(Responses.clarify).format(
            previous_question=Responses.fact_question(current_fact.name))

    # Commit
    db.session.commit()

    return jsonify({
        "message": question
    })


def __classify_claim_category(message, person_type):
    """
    Classifies the claim category based on a message.
    :param message: Message from user
    :return: Claim category key
    """

    classify_dict = rasaClassifier.classify_problem_category(message, person_type)
    log.debug(
        "\nClassify Claim Category\n\tPerson Type:{}\n\tMessage: {}\n\tDict: {}".format(person_type.__value__, message,
                                                                                        classify_dict))

    # Return the claim category, or None if the answer was insufficient in determining one
    if intentThreshold.is_sufficient(classify_dict):
        determined_claim_category = classify_dict['intent']
        return determined_claim_category['name']
    else:
        return None


def __extract_entity(current_fact_name, current_fact_type, message):
    """
    Extracts the value of a fact, based on the current fact
    :param current_fact_name: Which fact we are checking for i.e. is_student
    :param current_fact_type: The type of the fact we are checking i.e. FactType.BOOLEAN
    :param message: Message given by the user
    :return: The determined value for the fact specified
    """

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
        return fact_service.extract_fact_by_type(current_fact_type, classify_dict['intent'], classify_dict['entities'])
    else:
        return None
