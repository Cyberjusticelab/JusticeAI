from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from db import DbGateway
from decorators import ensure_json, ensure_key, handle_options_method

app = Flask(__name__)
CORS(app, origins=['http://localhost:3040', 'https://procezeus.ca'])

gateway = DbGateway('beta.db')
gateway.create_table()

QUESTION_LENGTH_LIMIT = 10000
EMAIL_LENGTH_LIMIT = 100


@app.route('/health', methods=['GET', 'OPTIONS'])
@handle_options_method
def health():
    return make_response()


@app.route('/question', methods=['POST', 'OPTIONS'])
@handle_options_method
@ensure_json
@ensure_key('question')
def post_question():
    data = request.get_json()
    if len(data['question']) > QUESTION_LENGTH_LIMIT:
        return make_response(jsonify(message="'question' value is too long."), 422)

    id = gateway.insert_anonymous_question(data['question'])
    return jsonify(id=id)


@app.route('/email', methods=['PUT', 'OPTIONS'])
@handle_options_method
@ensure_json
@ensure_key('email')
def put_email():
    data = request.get_json()
    if len(data['email']) > EMAIL_LENGTH_LIMIT:
        return make_response(jsonify(message="'email' value is too long."), 422)

    if 'id' in data and data['id']:
        id = gateway.update_email_by_id(data['id'], data['email'])
    else:
        id = gateway.insert_anonymous_email(data['email'])

    return jsonify(id=id)


@app.route('/subscription', methods=['PUT', 'OPTIONS'])
@handle_options_method
@ensure_json
@ensure_key('is_subscribed')
def put_subscription():
    data = request.get_json()
    if not isinstance(data['is_subscribed'], int):
        return make_response(jsonify(message="'is_subscribed' must be an integer."), 422)

    if 'id' in data and data['id']:
        id = gateway.update_subscription_by_id(data['id'], data['is_subscribed'])
    else:
        id = gateway.insert_anonymous_subscription(data['is_subscribed'])

    return jsonify(id=id)


@app.route('/legal', methods=['PUT', 'OPTIONS'])
@handle_options_method
@ensure_json
@ensure_key('is_legal_professional')
def put_legal_professional():
    data = request.get_json()
    if not isinstance(data['is_legal_professional'], int):
        return make_response(jsonify(message="'is_legal_professional' must be an integer."), 422)

    if 'id' in data and data['id']:
        id = gateway.update_legal_professional_by_id(data['id'], data['is_legal_professional'])
    else:
        id = gateway.insert_anonymous_legal_professional(data['is_legal_professional'])

    return jsonify(id=id)
