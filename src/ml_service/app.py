from flask import Flask, request, jsonify
from web.ml_controller import MlController

app = Flask(__name__)


@app.route("/predict", methods=['POST'])
def classify_claim_category():
    input_json = request.get_json()
    return jsonify(MlController.predict_outcome(input_json))


@app.route("/weights", methods=['GET'])
def get_ordered_weights():
    return jsonify(MlController.get_weighted_facts())


@app.route("/antifacts", methods=['GET'])
def get_anti_facts():
    return jsonify(MlController.get_anti_facts())


@app.route("/statistics", methods=['GET'])
def get_ml_metrics():
    return jsonify(MlController.get_ml_statistics())
