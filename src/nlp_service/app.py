from flask import Flask
from flask import jsonify
from flask import request
from models.question import QuestionOutput
from services.tenant_landlord_classifier import TenantLandlordClassifier
from services.problem_category_classifier import ProblemCategoryClassifier
from services.has_lease_expired_classifier import HasLeaseExpiredClassifier
from services.is_habitable_classifier import IsHabitableClassifier
from services.is_student_classifier import IsStudentClassifier
from services.is_tenant_dead_classifier import IsTenantDeadClassifier
from services.lease_term_type_classifier import LeaseTermTypeClassifier

app = Flask(__name__)

classifiers = {
    'tenant_landlord': TenantLandlordClassifier(),
    'problem_category': ProblemCategoryClassifier(),
    'has_lease_expired': HasLeaseExpiredClassifier(),
    'is_habitable': IsHabitableClassifier(),
    'is_student': IsStudentClassifier(),
    'is_tenant_dead': IsTenantDeadClassifier(),
    'lease_term_type': LeaseTermTypeClassifier()
}


@app.route("/problem_category", methods=['POST'])
def problemCategory():
    question_json = request.get_json()
    output = classifiers['problem_category'].classify(question_json['answer'])
    question = QuestionOutput(None, None, [output])
    return jsonify(question.__dict__)


@app.route("/fact_extract", methods=['POST'])
def fact_extract():
    question_json = request.get_json()
    facts = question_json['facts']
    outputFacts = []
    for fact in facts:
        if fact in classifiers.keys():
            outputFacts.append(
                classifiers[fact].classify(question_json['answer']))

    question = QuestionOutput(None, None, outputFacts)
    return jsonify(question.__dict__)
