from flask import Flask, request, abort, make_response, jsonify
from flask_cors import CORS
from flask_marshmallow import Marshmallow

import database

app = Flask(__name__)

# DB Setup
# db = database.connect(app, 'postgres', 'postgres', 'postgres', host="localhost")
db = database.connect(app, 'postgres', 'DEV_PASS_NOT_SECRET', 'postgres')
ma = Marshmallow(app)

# Cors Setup
CORS(app)

from controllers import conversationController


@app.route("/new", methods=['POST'])
def init_conversation():
    init_request = request.get_json()
    return conversationController.init_conversation(init_request['name'])


@app.route("/conversation", methods=['POST'])
def chat():
    chat_request = request.get_json()
    return conversationController.receive_message(chat_request['conversation_id'], chat_request['message'])


@app.route("/conversation/<conversation_id>", methods=['GET'])
def get_conversation(conversation_id=None):
    if conversation_id:
        return conversationController.get_conversation(conversation_id)
    else:
        abort(make_response(jsonify(message="Invalid request"), 400))
