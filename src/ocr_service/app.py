import os

from flask import Flask
from flask import request

from controllers import ocr_controller

from postgresql_db import database

# Flask Setup
app = Flask(__name__)

# DB Setup
db = database.connect(app, 'postgres', os.environ['POSTGRES_PASSWORD'], 'postgres')

"""
These functions establishes HTTP routes for the core functionality of the src/ocr_service/controllers/ocrController.py
The core functionality of classify_claim_category and classify_fact_value are explained further in the file mentioned above
"""


@app.route("/extract_text", methods=['POST'])
def extract_text():
    request_data = request.get_json()
    return ocr_controller.extract_text(request_data['conversation_id'], request_data['image_data'])

