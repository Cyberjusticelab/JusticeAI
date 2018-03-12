import os

from flask import Flask, request, abort, make_response, jsonify
from flask_cors import CORS
from postgresql_db import database

# Flask Setup
app = Flask(__name__)

# DB Setup
db = database.connect(app, 'postgres', os.environ['POSTGRES_PASSWORD'], 'postgres')

# Cors Setup
CORS(app)

from controllers import conversation_controller, legal_controller, feedback_controller


@app.route('/health', methods=['GET'])
def health():
    return make_response()


@app.route("/new", methods=['POST'])
def init_conversation():
    init_request = request.get_json()
    return conversation_controller.init_conversation(init_request['name'], init_request['person_type'])


@app.route("/conversation", methods=['POST'])
def chat():
    chat_request = request.get_json()
    return conversation_controller.receive_message(chat_request['conversation_id'], chat_request['message'])


@app.route("/conversation/<conversation_id>", methods=['GET'])
def get_conversation(conversation_id=None):
    if conversation_id:
        return conversation_controller.get_conversation(conversation_id)
    else:
        abort(make_response(jsonify(message="Invalid request"), 400))


@app.route("/conversation/<conversation_id>/report", methods=['GET'])
def get_conversation_report(conversation_id=None):
    if conversation_id:
        return conversation_controller.get_report(conversation_id)
    else:
        abort(make_response(jsonify(message="Invalid request"), 400))


@app.route("/conversation/<conversation_id>/resolved", methods=['GET'])
def get_conversation_resolved_facts(conversation_id=None):
    if conversation_id:
        return conversation_controller.get_fact_entities(conversation_id)
    else:
        abort(make_response(jsonify(message="Invalid request"), 400))


@app.route("/conversation/<conversation_id>/resolved/<fact_entity_id>", methods=['DELETE'])
def delete_conversation_resolved_fact(conversation_id=None, fact_entity_id=None):
    if conversation_id and fact_entity_id:
        return conversation_controller.delete_fact_entity(conversation_id, fact_entity_id)
    else:
        abort(make_response(jsonify(message="Invalid request"), 400))


@app.route("/conversation/<conversation_id>/files", methods=['GET', 'POST'])
def handle_files(conversation_id=None):
    if conversation_id:
        if request.method == 'GET':
            return conversation_controller.get_file_list(conversation_id)

        if request.method == 'POST':
            if 'file' not in request.files:
                abort(make_response(jsonify(message="No file provided"), 400))

            return conversation_controller.upload_file(conversation_id, request.files['file'])
    else:
        abort(make_response(jsonify(message="Invalid request"), 400))


@app.route("/store-user-confirmation", methods=['POST'])
def store_user_confirmation():
    data = request.get_json()
    return conversation_controller.store_user_confirmation(data['conversation_id'], data['confirmation'])


@app.route("/legal", methods=['GET'])
def get_legal_documents():
    return legal_controller.get_legal_documents()


@app.route("/feedback", methods=['POST'])
def save_feedback():
    data = request.get_json()
    return feedback_controller.save_feedback(data['feedback'])
