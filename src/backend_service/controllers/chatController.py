from app import db
from flask import jsonify
from models.models import Conversation


def init_conversation(name):
    conversation = Conversation(name=name)

    db.session.add(conversation)
    db.session.commit()

    return jsonify(
        {
            'name': conversation.name,
            'conversation_id': conversation.id
        }
    )


def chat_message(conversation_id, answer):
    conversation = Conversation.query.get(conversation_id)

    return jsonify(
        {
            'conversation_id': conversation.id,
            'message': "Hello there, %s. Your message was %s" % (conversation.name, answer),
        }
    )
