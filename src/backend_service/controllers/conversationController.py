from flask import jsonify, abort, make_response
from models.staticStrings import *
from models.models import *
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
            response_text = WelcomeStrings().pick().format(name=conversation.name)
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
    else:
        return "Hello there, {}. Your message was '{}'".format(conversation.name, message)


def _determine_person_type(conversation, message):
    person_type = None
    nlp_request = nlpService.tenant_landlord(message)

    for fact in nlp_request['facts']:
        person_type = fact['person_class']

    if person_type is not None:
        conversation.person_type = {
            'tenant': PersonType.TENANT,
            'landlord': PersonType.LANDLORD
        }[person_type]

        db.session.commit()

        return ProblemInquiryStrings().pick().format(name=conversation.name,
                                                     person_type=conversation.person_type.value.lower())
    else:
        return ClarifyStrings().pick()


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

        return CategoryInquiryStrings().pick().format(
            claim_category=conversation.claim_category.value.lower().replace("_", " "))
    else:
        return ClarifyStrings().pick()


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


# Questions for lease termination
lease_term_type = 'Is there a specified end date to your lease?'
has_lease_expired = 'Has the lease expired already?'
is_tenant_dead = 'Is the tenant dead?'
is_student = 'Are you a student?'
is_habitable = 'How would you describe your dwelling? Is it habitable?'

# Questions for rent change (excluding lease_term_type)
is_rent_in_lease = 'Is the rent specified in the lease?'
rent_in_lease_amount = 'What is the amount of the rent'

# Question for nonpayment - obviously not both in_default and over_three_weeks will be asked
in_default = "How long has it been since you haven't paid?"
over_three_weeks = "How long has it been since you haven't paid?"
has_abandoned = 'Have you seen your tenant?'
interest_allowed = ''
interest_term = ''
interest_max = ''

# Question for deposits
is_rent_advance = 'Has the rent been asked to be paid in advance?'
first_month_rent_paid = 'Is it only for the first month?'

# List the facts inside of lists with the name of the categories
lease_termination = ['lease_term_type',
                     'has_lease_expired',
                     'is_tenant_dead',
                     'is_student',
                     'is_habitable']

rent_change = ['lease_term_type',
               'is_rent_in_lease',
               'rent_in_lease_amount']

nonpayment = ['in_default',
              'over_three_weeks',
              'has_abandoned',
              'interest_allowed',
              'interest_term',
              'interest_max']

deposits = ['is_rent_advance',
            'first_month_rent_paid']
