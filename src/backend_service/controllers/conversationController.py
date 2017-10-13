from flask import jsonify, abort, make_response

from models.factService import FactService
from models.models import *
from models.staticStrings import *
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
    nlp_request = nlpService.fact_extract(['tenant_landlord'], message)

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
    fact, question = FactService.get_question(conversation.claim_category.value.lower(), resolved_facts)

    if fact is not None:
        # Update fact being asked
        conversation.current_fact = fact
        db.session.commit()
    else:
        fact_dump = ''.join(repr(conversation.facts))
        question = "FACT DUMP: {}".format(fact_dump)

    return question
