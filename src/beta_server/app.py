from flask import Flask, request, jsonify, make_response
from db import DbGateway
from decorators import ensure_json, ensure_key


app = Flask(__name__)

gateway = DbGateway('beta.db')
gateway.create_table()

QUESTION_LENGTH_LIMIT = 10000
EMAIL_LENGTH_LIMIT = 100

@app.route('/question', methods=['POST'])
@ensure_json
@ensure_key('question')
def post_question():
    data = request.get_json()
    if len(data['question']) > QUESTION_LENGTH_LIMIT:
        return make_response(jsonify(message="'question' value is too long."), 422)

    id = gateway.insert_anonymous_question(data['question'])
    return jsonify(id=id)

@app.route('/email', methods=['PUT'])
@ensure_json
@ensure_key('email')
@ensure_key('id')
def put_email():
    data = request.get_json()
    if len(data['email']) > EMAIL_LENGTH_LIMIT:
        return make_response(jsonify(message="'email' value is too long."), 422)

    id = gateway.update_email_by_id(data['id'], data['email'])
    return jsonify(id=id)

@app.route('/subscription', methods=['PUT'])
@ensure_json
@ensure_key('is_subscribed')
@ensure_key('id')
def put_subscription():
    data = request.get_json()
    if not isinstance(data['is_subscribed'], int):
        return make_response(jsonify(message="'is_subscribed' must be an integer."), 422)

    id = gateway.update_subscription_by_id(data['id'], data['is_subscribed'])
    return jsonify(id=id)

