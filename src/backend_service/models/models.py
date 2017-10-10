from app import db


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    person = db.Column(db.String(120), unique=True, nullable=True)
