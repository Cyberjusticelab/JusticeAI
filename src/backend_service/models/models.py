from enum import Enum
from marshmallow_enum import EnumField
from app import db, ma

'''
-----
Enums
-----
'''


class PersonType(Enum):
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"


class SenderType(Enum):
    USER = "USER"
    BOT = "BOT"


'''
-----------------
SQLAlchemy Models
-----------------
'''


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    person_type = db.Column(db.Enum(PersonType))
    messages = db.relationship('Message')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender_type = db.Column(db.Enum(SenderType), nullable=False)
    text = db.Column(db.Text, nullable=False)


'''
-------------------
Marshmallow Schemas
-------------------
'''


class MessageSchema(ma.ModelSchema):
    sender_type = EnumField(SenderType, by_value=True)

    class Meta:
        model = Message


class ConversationSchema(ma.ModelSchema):
    person_type = EnumField(PersonType, by_value=True)
    messages = ma.Nested(MessageSchema, many=True)

    class Meta:
        model = Conversation
