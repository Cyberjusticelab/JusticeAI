import datetime
from enum import Enum
from marshmallow_enum import EnumField
from app import db, ma

'''
-----
Enums
-----
'''


class SenderType(Enum):
    USER = "USER"
    BOT = "BOT"


class PersonType(Enum):
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"


class ClaimCategory(Enum):
    LEASE_TERMINATION = "LEASE_TERMINATION"
    RENT_CHANGE = "RENT_CHANGE"
    NONPAYMENT = "NONPAYMENT"
    DEPOSITS = "DEPOSITS"


'''
-----------------
SQLAlchemy Models
-----------------
'''


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    person_type = db.Column(db.Enum(PersonType))
    claim_category = db.Column(db.Enum(ClaimCategory))
    current_fact = db.Column(db.String(50))
    messages = db.relationship('Message')
    facts = db.relationship('Fact')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender_type = db.Column(db.Enum(SenderType), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    text = db.Column(db.Text, nullable=False)


class Fact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(50), nullable=False)


'''
-------------------
Marshmallow Schemas
-------------------
'''


class MessageSchema(ma.ModelSchema):
    # Enum
    sender_type = EnumField(SenderType, by_value=True)

    class Meta:
        model = Message


class FactSchema(ma.ModelSchema):
    class Meta:
        model = Fact


class ConversationSchema(ma.ModelSchema):
    # Enum
    person_type = EnumField(PersonType, by_value=True)
    claim_category = EnumField(ClaimCategory, by_value=True)

    # Lists
    messages = ma.Nested(MessageSchema, many=True)
    facts = ma.Nested(FactSchema, many=True)

    class Meta:
        model = Conversation
