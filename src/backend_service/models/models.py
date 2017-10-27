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


class DocumentType(Enum):
    LEASE = "LEASE"


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
    files = db.relationship('File')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender_type = db.Column(db.Enum(SenderType), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    file_request = db.relationship('FileRequest', uselist=False, backref='message')
    possible_answers = db.Column(db.Text)

    def request_file(self, document_type):
        file_request = FileRequest(document_type=document_type)
        self.file_request = file_request


class FileRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    document_type = db.Column(db.Enum(DocumentType), nullable=False)

    def __init__(self, document_type):
        self.document_type = document_type


class Fact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "{}:{}".format(self.name, self.value)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


# Create tables
print("Creating database tables from models.py")
db.create_all()

'''
-------------------
Marshmallow Schemas
-------------------
'''


class FileRequestSchema(ma.ModelSchema):
    # Enum
    document_type = EnumField(DocumentType, by_value=True)

    class Meta:
        fields = ['document_type']


class MessageSchema(ma.ModelSchema):
    # Enum
    sender_type = EnumField(SenderType, by_value=True)

    # One to one
    file_request = ma.Nested(FileRequestSchema)

    class Meta:
        model = Message


class FactSchema(ma.ModelSchema):
    class Meta:
        model = Fact


class FileSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'name', 'type', 'timestamp')


class ConversationSchema(ma.ModelSchema):
    # Enum
    person_type = EnumField(PersonType, by_value=True)
    claim_category = EnumField(ClaimCategory, by_value=True)

    # One to many
    messages = ma.Nested(MessageSchema, many=True)
    facts = ma.Nested(FactSchema, many=True)

    class Meta:
        fields = ('id', 'name', 'person_type', 'messages', 'facts')
