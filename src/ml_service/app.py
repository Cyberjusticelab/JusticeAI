from flask import Flask, request, jsonify
from web import ml_controller
app = Flask(__name__)


@app.route("/predict", methods=['POST'])
def classify_claim_category():
    input_json = request.get_json()
    return jsonify(ml_controller.predict_outcome(input_json))
