from flask import Flask, request, jsonify, make_response
from db import DbGateway
from decorators import ensure_json, ensure_key


app = Flask(__name__)

gateway = DbGateway('beta.db')
gateway.create_table()

QUESTION_LENGTH_LIMIT = 10000

@app.route('/question', methods=['POST'])
@ensure_json
@ensure_key('question')
def post_question():
    data = request.get_json()
    if len(data['question']) > QUESTION_LENGTH_LIMIT:
        return make_response(jsonify(message="'question' value is too long."), 422)

    id = gateway.insert_anonymous_question(data['question'])
    return jsonify(id=id)
