from flask import jsonify, abort, make_response

def process_user_input(conversation_id, message):

    if conversation_id is None or message is None:
        abort(make_response(jsonify(message="Must provide conversation_id and message"), 400))

    # Retrieve current_fact from conversation
    current_fact = __get_current_fact(conversation_id)

    # Extract entity from message based on current fact
    fact_entity = __extract_entity(current_fact, message)
    if fact_entity is None:
        return __generate_clarification_question()

    # Pass fact with extracted entity to ML service
    new_fact = None  # mlService.submit_resolved_fact(conversation_id, current_fact, fact_entity)

    # Set current_fact to new_fact (returned from ML service)
    __set_current_fact(conversation_id, new_fact)

    # Generate question for next fact (returned from ML service)
    question = __generate_question(new_fact)

    # Return question to backend
    response = {
        "message": question
    }
    pass  # return response


def __get_current_fact(conversation_id):
    return None


def __set_current_fact(conversation_id, new_fact):
    return None


def __extract_entity(current_fact, message):
    return None


def __generate_question(new_fact):
    return None


def __generate_clarification_question():
    return None
