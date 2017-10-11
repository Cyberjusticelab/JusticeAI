from flask import jsonify, abort, make_response
from models.staticStrings import *
from models.models import *


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
    return "Hello there, {}. Your message was '{}'".format(conversation.name, message)
