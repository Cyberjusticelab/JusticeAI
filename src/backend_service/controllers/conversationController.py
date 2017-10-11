from flask import jsonify, abort, make_response
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
        # Add user's message
        user_message = Message(sender_type=SenderType.USER, text=message)
        conversation.messages.append(user_message)

        # Generate a response message
        response_text = "Hello there, %s. Your message was '%s'" % (conversation.name, user_message.text)
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
