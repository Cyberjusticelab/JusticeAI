import os
import sys
from flask import jsonify, abort, make_response
from models.staticStrings import *
from models.models import *
from models.factService import FactService
from services import nlpService


def get_conversation(conversation_id):
    conversation = Conversation.query.get(conversation_id)
    if conversation:
        return ConversationSchema().jsonify(conversation)
    else:
        abort(make_response(jsonify(message="Conversation does not exist"), 404))


def init_conversation(name):
    conversation = Conversation(name=name)

    # Persist new conversation to DB
    db.session.add(conversation)
    db.session.commit()

    return jsonify(
        {
            'conversation_id': conversation.id
        }
    )


def receive_message(conversation_id, message):
    # Retrieve conversation
    conversation = Conversation.query.get(conversation_id)

    if conversation:

        # First message in the conversation
        if len(conversation.messages) == 0:
            response_text = StaticStrings.chooseFrom(StaticStrings.welcome).format(name=conversation.name)
        else:
            # Add user's message
            user_message = Message(sender_type=SenderType.USER, text=message)
            conversation.messages.append(user_message)
            response_text = _generate_response(conversation, user_message.text)

        # Persist response message
        response = Message(sender_type=SenderType.BOT, text=response_text)
        conversation.messages.append(response)

        # Commit
        db.session.commit()

        return jsonify(
            {
                'conversation_id': conversation.id,
                'message': response_text
            }
        )
    else:
        abort(make_response(jsonify(message="Conversation does not exist"), 404))


def _generate_response(conversation, message):
    if conversation.person_type is None:
        return _determine_person_type(conversation, message)
    elif conversation.claim_category is None:
        return _determine_claim_category(conversation, message)
    elif conversation.current_fact is not None:
        # Assume it is an answer to the current fact
        nlp_request = nlpService.fact_extract([conversation.current_fact], message=message)

        for resolved_fact in nlp_request['facts']:
            for fact_name, fact_value in resolved_fact.items():
                new_fact = Fact(name=fact_name, value=fact_value)
                conversation.facts.append(new_fact)

        db.session.commit()
        question = _probe_facts(conversation)
        return question


def _determine_person_type(conversation, message):
    person_type = None
    # nlp_request = nlpService.fact_extract(['person_class'], message) #TODO: CHANGE TO THIS AFTER PR
    nlp_request = nlpService.tenant_landlord(message)

    for fact in nlp_request['facts']:
        person_type = fact['tenant_landlord']

    if person_type is not None:
        conversation.person_type = {
            'tenant': PersonType.TENANT,
            'landlord': PersonType.LANDLORD
        }[person_type]

        db.session.commit()

        return StaticStrings.chooseFrom(StaticStrings.problem_inquiry).format(name=conversation.name,
                                                                              person_type=conversation.person_type.value.lower())
    else:
        return StaticStrings.chooseFrom(StaticStrings.clarify)


def _determine_claim_category(conversation, message):
    claim_category = None
    nlp_request = nlpService.problem_category(message)

    for fact in nlp_request['facts']:
        claim_category = fact['category']

    if claim_category is not None:
        conversation.claim_category = {
            'lease_termination': ClaimCategory.LEASE_TERMINATION,
            'rent_change': ClaimCategory.RENT_CHANGE,
            'nonpayment': ClaimCategory.NONPAYMENT,
            'deposits': ClaimCategory.DEPOSITS
        }[claim_category]

        db.session.commit()

        # Generate the first question
        first_question = _probe_facts(conversation)

        return StaticStrings.chooseFrom(StaticStrings.category_acknowledge).format(
            claim_category=conversation.claim_category.value.lower().replace("_", " "), first_question=first_question)
    else:
        return StaticStrings.chooseFrom(StaticStrings.clarify)


def _probe_facts(conversation):
    resolved_facts = [fact.name for fact in conversation.facts]
    fact, question = FactService.get_question(conversation.claim_category.lower(), resolved_facts)

    # Update fact being asked
    conversation.current_fact = fact
    db.session.commit()

    return question


# Mihai test stuff
# Dictionary to list converter

def dicttolist(dictionnaire):
    liste = []
    tempo = []
    newElementCheck = 0
    for key, value in dictionnaire.iteritems():
        newElementKey = key
        newElementValue = value
        tempo.extend(newElementKey)
        tempo.extend(newElementValue)
        tempo.extend(newElementCheck)
        liste.append(tempo)
        newElementKey = None
        newElementValue = None
        tempo[:] = []


# Model of every list of category: category = [fact, fact, fact, etc.] fact = [fact question, checked, value]
# Questions for lease termination
lease_term_type = ['Is there a specified end date to your lease?', False, None],
has_lease_expired = ['Has the lease expired already?', False, None],
is_tenant_dead = ['Is the tenant dead?', False, None],
is_student = ['Are you a student?', False, None],
is_habitable = ['How would you describe your dwelling? Is it habitable?', False, None]

# Questions for rent change (excluding lease_term_type)
is_rent_in_lease = ['Is the rent specified in the lease?', False, None]
rent_in_lease_amount = ['What is the amount of the rent', False, None]

# Question for nonpayment - obviously not both in_default and over_three_weeks will be asked
in_default = ""  # If you entered this category, you are automatically in default
over_three_weeks = ["How long has it been since you haven't paid?", False, None]
has_abandoned = ['Have you seen your tenant?', False, None]
interest_allowed = ''  # Not relevant for questioning
interest_term = ''  # Not relevant for questioning
interest_max = ''  # Not relevant for questioning

# Question for deposits
is_rent_advance = ['Has the rent been asked to be paid in advance?', False, None]
first_month_rent_paid = ['Is it only for the first month?', False, None]

# 1st part of the program
category = "lease_termination"  # Instantiate with the value of the category key
questionstoask = []


def initializeQuestions(category):
    if "lease_termination" in category:
        questionstoask.append(lease_term_type)
        questionstoask.append(has_lease_expired)
        questionstoask.append(is_tenant_dead)
        questionstoask.append(is_habitable)
    if "rent_change" in category:
        questionstoask.append(is_rent_in_lease, rent_in_lease_amount)
    if "nonpayment" in category:
        questionstoask.append(over_three_weeks, has_abandoned)
    if "deposits" in category:
        questionstoask.append(is_rent_advance, first_month_rent_paid)


# Run this everytime we get back an input from the user
def askQuestion():
    for facts in questionstoask:
        for x in facts:
            # if list is false (unchecked) or if the value wasn't instantiated, ask the question
            if x[1] is False:
                #  Dependency checker
                if canIAsk(x) is True:
                    # This will be replaced with the proper message
                    print(x[0])


# This will regulate what can be asked and what cannot be asked by dependency but will NOT regulate fact values changing
# Facts will uniquely be changed as a whole by the nlp_service without regulation or discrimination

def canIAsk(facts):
    # Write dependencies here for lease termination
    print(questionstoask[0][0][2])
    if "lease_termination" in category and facts in questionstoask:
        # Rule #1 cannot ask when it ends if it's indeterminate or the question about the type is not asked yet
        if "indeterminate" in (questionstoask[0][0][2]):
            return False
        else:
            return True
            # Write dependencies here for rent change
    elif "rent_change" in category and facts in questionstoask:
        # Rule #1 cannot ask what the rent in lease amount is if the rent is not in the lease
        if (questionstoask[1])[1] is False and facts in questionstoask:
            return False
        else:
            return True
            # Write dependencies here for nonpayment
    elif "nonpayment" in category and facts in questionstoask:
        return True
    # Write dependencies here for deposits
    elif "deposits" in category and facts in questionstoask:
        return True
    else:
        return True


initializeQuestions(category)
print(questionstoask)
askQuestion()
