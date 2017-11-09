import json

from flask import jsonify, abort, make_response

from models.models import *
from services import nlpService, fileService
from services.factService import FactService
from services.staticStrings import *


########################
# Conversation Handling
########################

def get_conversation(conversation_id):
    conversation = __get_conversation(conversation_id)

    return ConversationSchema().jsonify(conversation)


def init_conversation(name, person_type):
    if person_type.upper() not in PersonType.__members__:
        return abort(make_response(jsonify(message="Invalid person type provided"), 400))

    conversation = Conversation(name=name, person_type=PersonType[person_type.upper()])

    # Persist new conversation to DB
    db.session.add(conversation)
    db.session.commit()

    return jsonify(
        {
            'conversation_id': conversation.id
        }
    )


def receive_message(conversation_id, message):
    conversation = __get_conversation(conversation_id)

    response_text = None
    response_html = None
    file_request = None
    possible_answers = None
    additional_info = None
    enforce_possible_answer = False
    # First message in the conversation
    if len(conversation.messages) == 0:
        response_html = StaticStrings.chooseFrom(StaticStrings.disclaimer).format(name=conversation.name)
        possible_answers = json.dumps(["Yes"])
        enforce_possible_answer = True
    else:
        # Add user's message
        user_message = Message(sender_type=SenderType.USER, text=message)
        conversation.messages.append(user_message)

        # Generate response text & optional parameters
        response = __generate_response(conversation, user_message.text)
        response_text = response.get('response_text')
        file_request = response.get('file_request')
        possible_answers = response.get('possible_answers')

    # Persist response message
    if response_text is not None:
        response = Message(
            sender_type=SenderType.BOT,
            text=response_text,
            possible_answers=possible_answers,
            enforce_possible_answer=enforce_possible_answer
        )
    elif response_html is not None:
        response = Message(
            sender_type=SenderType.BOT,
            text=response_html,
            possible_answers=possible_answers,
            enforce_possible_answer=enforce_possible_answer
        )
    else:
        return abort(make_response(jsonify(message="Response text not generated"), 400))

    # Create relationship between message and file request if present
    if file_request is not None:
        response.file_request = file_request

    conversation.messages.append(response)

    # Commit
    db.session.commit()

    # Build response dict
    response_dict = {'conversation_id': conversation.id}

    if response_text is not None:
        response_dict['message'] = response_text
    if response_html is not None:
        response_dict['html'] = response_html
    if file_request is not None:
        response_dict['file_request'] = FileRequestSchema().dump(file_request).data
    if possible_answers is not None:
        response_dict['possible_answers'] = possible_answers
        if enforce_possible_answer:
            response_dict['enforce_possible_answer'] = True

    return jsonify(response_dict)


################
# File Handling
################

def get_file_list(conversation_id):
    conversation = __get_conversation(conversation_id)

    return jsonify(
        {
            'files': [FileSchema().dump(file).data for file in conversation.files]
        }
    )


def upload_file(conversation_id, file):
    conversation = __get_conversation(conversation_id)

    # Check if the file has a filename
    if file.filename == '':
        abort(make_response(jsonify(message="No file selected"), 400))

    if fileService.is_accepted_format(file):
        # Create the file and commit it to generate id
        new_file = File(name=fileService.sanitize_name(file), type=file.content_type)
        conversation.files.append(new_file)
        db.session.commit()

        # Generate path information and upload file to disk
        new_file.path = fileService.generate_path(conversation.id, new_file.id)
        fileService.upload_file(file, new_file.path, new_file.name)
        db.session.commit()

        # Return the file info
        return FileSchema().jsonify(new_file)
    else:
        abort(make_response(
            jsonify(message="Filetype {} is not supported. Supported filetypes are {}.".format(
                fileService.get_file_extension(file), fileService.get_accepted_formats_string())), 400))


##################
# Private Methods
##################

def __get_conversation(conversation_id):
    conversation = Conversation.query.get(conversation_id)

    if conversation:
        return conversation

    abort(make_response(jsonify(message="Conversation does not exist"), 404))


def __generate_response(conversation, message):
    if __has_just_accepted_disclaimer(conversation):
        return __ask_initial_question(conversation)
    elif conversation.claim_category is None:
        return __determine_claim_category(conversation, message)
    elif conversation.current_fact is not None:
        # Assume it is an answer to the current fact
        nlp_request = nlpService.submit_message([conversation.current_fact], message=message)

        for resolved_fact in nlp_request['facts']:
            for fact_name, fact_value in resolved_fact.items():
                new_fact = Fact(name=fact_name, value=fact_value)
                conversation.facts.append(new_fact)

        db.session.commit()
        question = __probe_facts(conversation)

        return {'response_text': question}


def __ask_initial_question(conversation):
    person_type = conversation.person_type

    file_request = None
    if person_type is PersonType.TENANT:
        file_request = FileRequest(document_type=DocumentType.LEASE)

    db.session.commit()

    # Generate response based on person type
    response = None
    if person_type is PersonType.TENANT:
        response = StaticStrings.chooseFrom(StaticStrings.problem_inquiry_tenant).format(name=conversation.name)
    elif person_type is PersonType.LANDLORD:
        response = StaticStrings.chooseFrom(StaticStrings.problem_inquiry_landlord).format(name=conversation.name)

    return {'response_text': response, 'file_request': file_request}


def __determine_claim_category(conversation, message):
    claim_category = None
    nlp_request = nlpService.claim_category(conversation.id, message)

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
        first_question = __probe_facts(conversation)

        response = StaticStrings.chooseFrom(StaticStrings.category_acknowledge).format(
            claim_category=conversation.claim_category.value.lower().replace("_", " "), first_question=first_question)

        return {'response_text': response}
    else:
        return {'response_text': StaticStrings.chooseFrom(StaticStrings.clarify)}


def __probe_facts(conversation):
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


def __has_just_accepted_disclaimer(conversation):
    return len(conversation.messages) == 2
