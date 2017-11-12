from flask import jsonify, abort, make_response

import util

util.load_src_dir_to_sys_path()
from db_state_service.models import *
from rasa.rasa_classifier import RasaClassifier
from services import mlService
from services.responseStrings import Responses

from nlp_service.app import db

# Global Variables

# Decided value of 30% percent difference (which is used for the reprompt and calculated from the percent difference: |First-Second|/[1/2(First+Second)]
# The first and the second are described by the the #1 and #2 intent returned by the Rasa's SVM intent calculation
minimum_percent_difference = 0.3

# Rasa Classifier - Initialization of Rasa Classifier to train the data and produce the required models per facts
rasaClassifier = RasaClassifier()
rasaClassifier.train(force_train=True)

"""
       Classify the claim and bring back a category between rent change, lease termination, nonpayment and deposits
        conversation_id: The id of the conversation inside of the database (i-->i++ on a new conversation)
        message: message given to classify between the previously mentionned categories
        returns: return a jsonified formatted message holding the category and the first question to be shown to the user
"""


def classify_claim_category(conversation_id, message):
    if conversation_id is None or message is None:
        abort(make_response(jsonify(message="Must provide conversation_id and message"), 400))

    # Retrieve conversation
    conversation = db.session.query(Conversation).get(conversation_id)

    # Classify claim category based on message
    claim_category = __classify_claim_category(message)

    # Set conversation's claim category
    conversation.claim_category = {
        'ask_lease_termination': ClaimCategory.LEASE_TERMINATION,
        'ask_rent_change': ClaimCategory.RENT_CHANGE,
        'ask_nonpayment': ClaimCategory.NONPAYMENT,
        'ask_deposit': ClaimCategory.DEPOSITS
    }[claim_category]

    # Get first fact based on claim category
    ml_request = mlService.submit_claim_category(conversation.claim_category)
    first_fact_id = ml_request['fact_id']

    # Retrieve the Fact from DB
    first_fact = db.session.query(Fact).get(first_fact_id)

    # Save first fact as current fact
    conversation.current_fact = first_fact

    # Commit
    db.session.commit()

    # Generate next message
    first_fact_question = Responses.fact_question(first_fact.name)
    message = Responses.chooseFrom(Responses.category_acknowledge).format(
        claim_category=conversation.claim_category.value.lower().replace("_", " "),
        first_question=first_fact_question)

    return jsonify({
        "message": message
    })


'''
    This service chooses the next question to be asked to the client after the category is chosen in classify_claim_category
        conversation_id: ID of the conversation
        message: message given by the user to the system
        :returns back the next question in the flow of the conversation with the user
'''


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
        ml_request = mlService.submit_resolved_fact(conversation, current_fact, fact_entity_value)
        new_fact_id = ml_request['fact_id']

        # Retrieve the Fact from DB
        if new_fact_id:
            new_fact = db.session.query(Fact).get(new_fact_id)

            # Set current_fact to new_fact (returned from ML service)
            conversation.current_fact = new_fact

            # Generate question for next fact (returned from ML service)
            question = Responses.fact_question(new_fact.name)
        else:
            question = "FACT DUMP: "
            for fact_entity in conversation.fact_entities:
                question += "{}:{}, ".format(fact_entity.fact.name, fact_entity.value)
    else:
        question = Responses.chooseFrom(Responses.clarify)

    # Commit
    db.session.commit()

    return jsonify({
        "message": question
    })


'''
        Extracting method that will return the claim category by name if the intent percentage difference is satisfactory
        message: message inputted by the user
        :returns the name of a problem category 
'''


def __classify_claim_category(message):
    classify_dict = rasaClassifier.classify_problem_category(message)
    print(classify_dict)

    # Return the claim category, or None if the answer was insufficient in determining one
    if __is_answer_sufficient(classify_dict):
        determined_problem_category = classify_dict['intent']
        print("Confidence: {}%".format(round(determined_problem_category['confidence'], 3) * 100))
        print("Intent: {}".format(determined_problem_category['name']))
        return determined_problem_category['name']
    else:
        return None


'''
    Method which extracts the intent of the message that was inputted by the user
    current_fact_name: which fact we are checking for i.e. is_student
    message: the message given by the user
    :returns the name of the intent

'''


def __extract_entity(current_fact_name, message):
    classify_dict = rasaClassifier.classify_fact(current_fact_name, message)
    print(classify_dict)

    # Return the fact value, or None if the answer was insufficient in determining one
    if __is_answer_sufficient(classify_dict):
        determined_intent = classify_dict['intent']
        print("Confidence: {}%".format(round(determined_intent['confidence'], 3) * 100))
        print("Intent: {}".format(determined_intent['name']))
        return determined_intent['name']
    else:
        return None


'''
    Method which verifies the accuracy of the classification with a percentage difference between the intent with the largest confidence and the intent with the 2nd largest confidence
    classify_dict: the dict holding the intents, classification %, entities
    :returns False if percentage difference is below 30%
'''


# Determine confidence of returned intent
def __is_answer_sufficient(classify_dict):
    if len(classify_dict['intent_ranking']) > 1:
        percent_difference = RasaClassifier.intent_percent_difference(classify_dict)
        print("Percent Difference: {}%".format(round(percent_difference, 3) * 100))
        if percent_difference < minimum_percent_difference:
            return False
    return True
