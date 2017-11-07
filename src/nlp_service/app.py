from flask import Flask
from flask import jsonify
from flask import request

from controllers import nlpController

app = Flask(__name__)


@app.route("/submit_answer", methods=['POST'])
def submit_answer():
    input = request.get_json()
    next_message = nlpController.process_user_input(input['conversation_id'], input['message'])
    return jsonify({'message': next_message})
