from postgresql_db.models import *
from flask import jsonify
from app import db


def save_feedback(feedback_text):
    feedback = Feedback(feedback=feedback_text)
    db.session.add(feedback)
    db.session.commit()
    return jsonify({"success": True})