import flask
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
    conversation = __get_conversation(conversation_id)

    response_text = None
    response_html = None
    file_request = None
    possible_answers = None
    additional_info = None
    hide_text_input = False
    # First message in the conversation
    if len(conversation.messages) == 0:
        response_html = StaticStrings.chooseFrom(StaticStrings.disclaimer).format(name=conversation.name)
        possible_answers = ["Yes"]
        hide_text_input = True
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
        response = Message(sender_type=SenderType.BOT, text=response_text)
    elif response_html is not None:
        response = Message(sender_type=SenderType.BOT, text=response_html)
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
    if hide_text_input:
        response_dict['hide_text_input'] = True

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


def get_file(conversation_id, file_id):
    conversation = __get_conversation(conversation_id)

    for file in conversation.files:
        if file.id == int(file_id):
            return flask.send_from_directory(file.path, file.name, mimetype=file.type, as_attachment=True)

    return abort(make_response(jsonify(message="File does not exist"), 404))


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
        response_text = StaticStrings.chooseFrom(StaticStrings.welcome).format(name=conversation.name)
        return {'response_text': response_text}
    if conversation.person_type is None:
        return __determine_person_type(conversation, message)
    elif conversation.claim_category is None:
        return __determine_claim_category(conversation, message)
    elif conversation.current_fact is not None:
        # Assume it is an answer to the current fact
        nlp_request = nlpService.fact_extract([conversation.current_fact], message=message)

        for resolved_fact in nlp_request['facts']:
            for fact_name, fact_value in resolved_fact.items():
                new_fact = Fact(name=fact_name, value=fact_value)
                conversation.facts.append(new_fact)

        db.session.commit()
        question = __probe_facts(conversation)

        return {'response_text': question}


def __determine_person_type(conversation, message):
    person_type = None
    nlp_request = nlpService.fact_extract(['tenant_landlord'], message)

    for fact in nlp_request['facts']:
        person_type = fact['tenant_landlord']

    if person_type is not None:
        conversation.person_type = {
            'tenant': PersonType.TENANT,
            'landlord': PersonType.LANDLORD
        }[person_type]

        file_request = None
        if person_type == 'tenant':
            file_request = FileRequest(document_type=DocumentType.LEASE)

        db.session.commit()

        # Generate response based on person type
        response = None
        if person_type == 'tenant':
            response = StaticStrings.chooseFrom(StaticStrings.problem_inquiry_tenant).format(name=conversation.name)
        elif person_type == 'landlord':
            response = StaticStrings.chooseFrom(StaticStrings.problem_inquiry_landlord).format(name=conversation.name)

        return {'response_text': response, 'file_request': file_request}
    else:
        return {'response_text': StaticStrings.chooseFrom(StaticStrings.clarify)}


def __determine_claim_category(conversation, message):
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
