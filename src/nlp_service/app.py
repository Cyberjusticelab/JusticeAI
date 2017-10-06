from flask import Flask
from flask import jsonify
from flask import request
from models.question import QuestionInput
from models.introduction import IntroductionInput
from services.yes_no_classifier import YesNoClassifier
from services.introduction_parser import IntroductionParser

app = Flask(__name__)


@app.route("/introduction", methods=['POST'])
def introduction():
  introduction_json = request.get_json()
  introduction = IntroductionInput(introduction_json['conversation_id'],
                                   introduction_json['name'],
                                   introduction_json['person'])
  output = IntroductionParser.classify(introduction)
  return jsonify(output.__dict__)


@app.route("/yesno", methods=['POST'])
def yesno():
    question_json = request.get_json()
    question = QuestionInput(question_json['question_id'],
                             question_json['conversation_id'],
                             question_json['answer'])
    output = YesNoClassifier.classify(question)
    return jsonify(output.__dict__)


@app.route("/openended")
def openended():
    return jsonify(implemented="NOT REALLY")
