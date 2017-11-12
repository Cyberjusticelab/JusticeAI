import os

from flask import Flask
from flask import request

import util
from controllers import nlpController

util.load_src_dir_to_sys_path()
from shared_modules import database

# Flask Setup
app = Flask(__name__)

# DB Setup
db = database.connect(app, 'postgres', os.environ['POSTGRES_PASSWORD'], 'postgres')


@app.route("/claim_category", methods=['POST'])
def classify_claim_category():
    input = request.get_json()
    return nlpController.classify_claim_category(input['conversation_id'], input['message'])


@app.route("/submit_message", methods=['POST'])
def submit_message():
    input = request.get_json()
    return nlpController.classify_fact_value(input['conversation_id'], input['message'])
