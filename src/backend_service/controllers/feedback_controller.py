from postgresql_db.models import *
from flask import jsonify
from app import db


def save_feedback(data):
    info = Feedback(feedback=data)
    db.session.add(info)
    db.session.commit()
    return jsonify({"success": True})