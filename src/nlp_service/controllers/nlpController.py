from flask import jsonify, abort, make_response

from models.models import Conversation


def classify_claim_category(conversation_id, message):
    if conversation_id is None or message is None:
        abort(make_response(jsonify(message="Must provide conversation_id and message"), 400))

    # Classify claim category based on message

    # Set conversation's claim category

    question = None
    
    return jsonify({
        "message": question
    })


def process_user_input(conversation_id, message):
    if conversation_id is None or message is None:
        abort(make_response(jsonify(message="Must provide conversation_id and message"), 400))

    # Retrieve conversation
    conversation = __get_conversation(conversation_id)

    # Retrieve current_fact from conversation
    current_fact = conversation.current_fact

    # Extract entity from message based on current fact
    question = None

    fact_entity_value = __extract_entity(current_fact, message)
    if fact_entity_value is not None:
        # Pass fact with extracted entity to ML service
        new_fact = None  # mlService.submit_resolved_fact(conversation_id, current_fact, fact_entity)

        # Set current_fact to new_fact (returned from ML service)
        # __set_current_fact(conversation_id, new_fact)

        # Generate question for next fact (returned from ML service)
        question = __generate_question(new_fact)
    else:
        question = __generate_clarification_question()

    return jsonify({
        "message": question
    })


def __get_conversation(conversation_id):
    return Conversation.query.get(conversation_id)


def __extract_entity(current_fact, message):
    # Rasa stuff happens here
    return 'some entity value'


def __generate_question(new_fact):
    return "Please gimmie stuff"


def __generate_clarification_question():
    return "Please clarify stuff"
