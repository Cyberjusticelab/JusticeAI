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

# The maximum of additional facts to ask before giving a new prediction
MAX_ADDITIONAL_FACTS = 5


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

    conversation_progress = None
    if claim_category in Responses.static_claim_responses.keys():
        response = Responses.faq_statement(claim_category, conversation.person_type.value)
    elif claim_category:
        # Set conversation's claim category
        conversation.claim_category = {
            'ask_lease_termination': ClaimCategory.LEASE_TERMINATION,
            'ask_nonpayment': ClaimCategory.NONPAYMENT,
            'ask_retake_rental': ClaimCategory.RETAKE_RENTAL
        }[claim_category]

        # Get first fact based on claim category
        first_fact = fact_service.submit_claim_category(conversation)
        first_fact_id = first_fact['fact_id']

        if first_fact_id:
            # Retrieve the Fact from DB
            first_fact = db.session.query(Fact).get(first_fact_id)

            # Save first fact as current fact
            conversation.current_fact = first_fact

            # Set conversation bot state
            conversation.bot_state = BotState.RESOLVING_FACTS

            # Commit
            db.session.commit()

            # Generate next message
            first_fact_question = Responses.fact_question(first_fact.name)
            response = Responses.chooseFrom(Responses.category_acknowledge).format(
                claim_category=conversation.claim_category.value.lower().replace("_", " "),
                first_question=first_fact_question)

            # Calculate the conversation progress
            conversation_progress = __calculate_conversation_progress(conversation)
        else:
            response = Responses.chooseFrom(Responses.category_acknowledge).format(
                claim_category=conversation.claim_category.value.lower().replace("_", " "),
                first_question=Responses.chooseFrom(Responses.unimplemented_category_error))
    else:
        response = Responses.chooseFrom(Responses.clarify).format(previous_question="")

    return jsonify({
        "message": response,
        "conversation_progress": conversation_progress
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

    # Question to return
    question = None

    just_acknowledged = False
    if conversation.bot_state is BotState.AWAITING_ACKNOWLEDGEMENT:
        question, just_acknowledged = __state_awaiting_acknowledgement(conversation, message)

    if conversation.bot_state is BotState.RESOLVING_FACTS:
        question = __state_resolving_facts(conversation, message)

    if conversation.bot_state is BotState.RESOLVING_ADDITIONAL_FACTS:
        question = __state_resolving_additional_facts(conversation, message, just_acknowledged)

    if conversation.bot_state is BotState.GIVING_PREDICTION:
        question = __state_giving_prediction(conversation)

    # Commit
    db.session.commit()

    return jsonify({
        "message": question,
        "conversation_progress": __calculate_conversation_progress(conversation)
    })


def __state_awaiting_acknowledgement(conversation, message):
    """
    Bot is waiting for an acknowledgement from the user
    :param conversation: The current conversation
    :param message: The user's message
    :return: Tuple: a question to ask, a flag determining whether or not an acknowledgement has just happened
    """

    question = None
    just_acknowledged = False
    if conversation.bot_state is BotState.AWAITING_ACKNOWLEDGEMENT:
        should_continue = __classify_acknowledgement(message)

        if should_continue is not None:
            if should_continue:
                conversation.bot_state = BotState.RESOLVING_ADDITIONAL_FACTS
                just_acknowledged = True
            else:
                conversation.bot_state = BotState.DETERMINE_CLAIM_CATEGORY
                question = Responses.prompt_reset_flow(conversation.person_type.value)
        else:
            question = Responses.chooseFrom(Responses.clarify)

    return question, just_acknowledged


def __state_resolving_facts(conversation, message):
    """
    Bot is asking the user question to resolve important facts
    :param conversation: The current conversation
    :param message: The user's message
    :return: A question to ask
    """

    question = None

    # Retrieve current_fact from conversation
    current_fact = conversation.current_fact

    # Extract entity from message based on current fact
    fact_entity_value = __extract_entity(current_fact.name, current_fact.type, message)

    if fact_entity_value is not None:
        next_fact = fact_service.submit_resolved_fact(conversation, current_fact, fact_entity_value)
        new_fact_id = next_fact['fact_id']

        if new_fact_id:
            new_fact = db.session.query(Fact).get(new_fact_id)
            conversation.current_fact = new_fact

            if fact_service.has_important_facts(conversation):
                # Important facts remain to be asked
                question = Responses.fact_question(new_fact.name)
            else:
                # There are no more important facts! Give a prediction
                conversation.bot_state = BotState.GIVING_PREDICTION
    else:
        question = Responses.chooseFrom(Responses.clarify).format(
            previous_question=Responses.fact_question(current_fact.name))

    return question


def __state_resolving_additional_facts(conversation, message, just_acknowledged):
    """
    Bot is asking the user questions to resolve additional facts
    :param conversation: The current conversation
    :param message: The user's message
    :param just_acknowledged: Whether or not an acknowledgement just happened.
        Used to skip fact resolution and instead asks a question immediately.
    :return: A question to as
    """

    question = None

    # Retrieve current_fact from conversation
    current_fact = conversation.current_fact

    if just_acknowledged:
        question = Responses.fact_question(current_fact.name)
    else:
        # Extract entity from message based on current fact
        fact_entity_value = __extract_entity(current_fact.name, current_fact.type, message)

        if fact_entity_value is not None:
            next_fact = fact_service.submit_resolved_fact(conversation, current_fact, fact_entity_value)
            new_fact_id = next_fact['fact_id']

            new_fact = None
            if new_fact_id:
                new_fact = db.session.query(Fact).get(new_fact_id)
                conversation.current_fact = new_fact

            # Additional facts remain to be asked
            if fact_service.has_additional_facts(conversation):
                # Additional fact limit reached, time for a new prediction
                if fact_service.count_additional_facts_resolved(conversation) % MAX_ADDITIONAL_FACTS == 0:
                    conversation.bot_state = BotState.GIVING_PREDICTION
                else:
                    question = Responses.fact_question(new_fact.name)
            else:
                # There are no more additional facts! Give a prediction
                conversation.bot_state = BotState.GIVING_PREDICTION

    return question


def __state_giving_prediction(conversation):
    """
    Bot has been told to give a prediction. If additional questions remain, will set the bot to wait for an acknowledgement.
    :param conversation: The current conversation
    :return: A prediction given answered facts
    """
    question = None

    # Submit request to ML service for prediction
    ml_response = ml_service.submit_resolved_fact_list(conversation)

    # Extract relevant data from the ml response
    ml_prediction = ml_service.extract_prediction(ml_response=ml_response)
    similar_precedent_list = ml_response['similar_precedents']

    # Generate statement for prediction
    question = Responses.prediction_statement(
        claim_category_value=conversation.claim_category.value,
        prediction_dict=ml_prediction,
        similar_precedent_list=similar_precedent_list)

    # If there are additional questions to be asked
    if fact_service.has_additional_facts(conversation):
        # Set the bot state
        conversation.bot_state = BotState.AWAITING_ACKNOWLEDGEMENT

        # Append to the question
        total_unresolved_additional = fact_service.count_additional_facts_unresolved(conversation)

        if total_unresolved_additional >= MAX_ADDITIONAL_FACTS:
            additional_question_count = MAX_ADDITIONAL_FACTS
        else:
            additional_question_count = total_unresolved_additional

        question = question + Responses.prompt_additional_questions(additional_question_count)
    else:
        # Set the bot state
        conversation.bot_state = BotState.DETERMINE_CLAIM_CATEGORY

        # Append to the question
        question = question + Responses.prompt_reset_flow(conversation.person_type.value, separate_message=True)

    return question


def __calculate_conversation_progress(conversation):
    """
    Calculates the conversation progress for a conversation.
    :param conversation: The current conversation
    :return: A percentage number that is set to 100% once all important facts are resolved.
    Then decreased if additional facts should be answered.
    """
    conversation_progress = 0
    important_fact_count = len(fact_service.get_category_fact_list(conversation.claim_category.value)["facts"])
    resolved_important_fact_count = fact_service.count_important_facts_resolved(conversation)

    if conversation.bot_state is BotState.GIVING_PREDICTION or conversation.bot_state is BotState.AWAITING_ACKNOWLEDGEMENT:
        conversation_progress = 1
    elif conversation.bot_state is BotState.DETERMINE_CLAIM_CATEGORY:
        conversation_progress = None
    elif conversation.bot_state is BotState.RESOLVING_FACTS:
        conversation_progress = resolved_important_fact_count / important_fact_count
    elif conversation.bot_state is BotState.RESOLVING_ADDITIONAL_FACTS:
        resolved_additional_fact_count = fact_service.count_additional_facts_resolved(conversation)

        unresolved_additional_fact_count = fact_service.count_additional_facts_unresolved(conversation)
        if unresolved_additional_fact_count >= MAX_ADDITIONAL_FACTS:
            additional_facts = MAX_ADDITIONAL_FACTS
        else:
            additional_facts = unresolved_additional_fact_count

        conversation_progress = (resolved_important_fact_count + resolved_additional_fact_count) / \
                                (important_fact_count + additional_facts)
    if conversation_progress is None:
        return conversation_progress
    else:
        return int(conversation_progress * 100)


def __classify_acknowledgement(message):
    """
    Classifies an acknowledgement. Can result in a True or False. Uses the additional_fact_acknowledgement data set.
    :param message: A user's message
    :return: True or False if classification was successful. None if clarification required.
    """

    classify_dict = rasaClassifier.classify_acknowledgement(message)
    log.debug(
        "\nClassify Acknowledgement\n\tMessage: {}\n\tOutput: {}".format(message, classify_dict))

    if intentThreshold.is_sufficient(classify_dict):
        determined_acknowledgement = classify_dict['intent']['name']
        if determined_acknowledgement == "true":
            return True
        elif determined_acknowledgement == "false":
            return False

    return None


def __classify_claim_category(message, person_type):
    """
    Classifies the claim category based on a message and person type.
    :param message: Message from user
    :param person_type: User's PersonType AS A STRING. i.e: "TENANT"
    :return: Classified claim category key. None if clarification required.
    """

    classify_dict = rasaClassifier.classify_problem_category(message, person_type)
    log.debug(
        "\nClassify Claim Category\n\tPerson Type: {}\n\tMessage: {}\n\tOutput: {}".format(person_type, message,
                                                                                           classify_dict))

    # Return the claim category, or None if the answer was insufficient in determining one
    if intentThreshold.is_sufficient(classify_dict):
        determined_claim_category = classify_dict['intent']
        return determined_claim_category['name']

    return None


def __extract_entity(current_fact_name, current_fact_type, message):
    """
    Extracts the value of a fact, based on the current fact
    :param current_fact_name: Which fact we are checking for i.e. is_student
    :param current_fact_type: The type of the fact we are checking i.e. FactType.BOOLEAN
    :param message: Message given by the user
    :return: The determined value for the fact specified. None if clarification required.
    """

    # First pass: outlier detection
    # TODO: For now, this is disabled while we are gathering data from beta users
    if 'OUTLIER_DETECTION' in os.environ:
        result = outlier_detector.predict_if_outlier([message.lower()])
        if result[0] == -1:
            return None

    classify_dict = rasaClassifier.classify_fact(current_fact_name, message)
    log.debug("\nClassify Fact\n\tMessage: {}\n\tFact Name: {}\n\tOutput: {}".format(message, current_fact_name,
                                                                                     classify_dict))

    # Return the fact value, or None if the answer was insufficient in determining one
    if intentThreshold.is_sufficient(classify_dict):
        return fact_service.extract_fact_by_type(current_fact_type, classify_dict['intent'], classify_dict['entities'])

    return None
