from flask import Flask
from flask import jsonify
from flask import request
from models.question import QuestionInput
from models.introduction import IntroductionInput
from services.yes_no_classifier import YesNoClassifier
from services.introduction_parser import IntroductionParser
from services.tenant_landlord_classifier import TenantLandlordClassifier
from services.problem_category_classifier import ProblemCategoryClassifier

app = Flask(__name__)

tenantLandlordClassifier = TenantLandlordClassifier()
problemCategoryClassifier = ProblemCategoryClassifier()


@app.route("/introduction", methods=['POST'])
def introduction():
    introduction_json = request.get_json()
    introduction = IntroductionInput(introduction_json['conversation_id'],
                                     introduction_json['name'],
                                     introduction_json['person'])
    output = IntroductionParser.classify(introduction)
    return jsonify(output.__dict__)


@app.route("/tenant_landlord", methods=['POST'])
def tenantLandlord():
    question_json = request.get_json()
    question = QuestionInput(None, None, question_json['answer'])
    output = tenantLandlordClassifier.classify(question)
    return jsonify(output.__dict__)


@app.route("/problem_category", methods=['POST'])
def problemCategory():
    question_json = request.get_json()
    question = QuestionInput(None, None, question_json['answer'])
    output = problemCategoryClassifier.classify(question)
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
