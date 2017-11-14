import os

from flask import Flask
from flask import request

from controllers import nlpController

from postgresql_db import database

# Flask Setup
app = Flask(__name__)

# DB Setup
db = database.connect(app, 'postgres', os.environ['POSTGRES_PASSWORD'], 'postgres')

"""
  These functions establishes HTTP routes for the core functionality of the src/nlp_service/controllers/nlpController.py
  The core functionality of classify_claim_category and classify_fact_value are explained further in the file mentioned above

"""


@app.route("/claim_category", methods=['POST'])
def classify_claim_category():
    input = request.get_json()
    return nlpController.classify_claim_category(input['conversation_id'], input['message'])


@app.route("/submit_message", methods=['POST'])
def submit_message():
    input = request.get_json()
    return nlpController.classify_fact_value(input['conversation_id'], input['message'])
