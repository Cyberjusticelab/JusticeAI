import datetime
from enum import Enum

from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow_enum import EnumField

import postgresql_db.database as database

app = Flask(__name__)
db = database.connect(app, 'postgres', 'postgres', 'postgres', host='127.0.0.1')
ma = Marshmallow(app)

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


class FactType(Enum):
    TEXT = "TEXT"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    MONEY = "MONEY"


class DocumentType(Enum):
    LEASE = "LEASE"


'''
-----------------
SQLAlchemy Models
-----------------
'''


class Fact(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum(FactType), nullable=False)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    name = db.Column(db.String(40), nullable=False)
    person_type = db.Column(db.Enum(PersonType))
    claim_category = db.Column(db.Enum(ClaimCategory))

    # One to one
    current_fact_id = db.Column(db.Integer, db.ForeignKey('fact.id'))
    current_fact = db.relationship('Fact', uselist=False, backref='conversation')

    # One to many
    messages = db.relationship('Message')
    fact_entities = db.relationship('FactEntity')
    files = db.relationship('File')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))

    # Attributes
    sender_type = db.Column(db.Enum(SenderType), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    possible_answers = db.Column(db.Text)
    enforce_possible_answer = db.Column(db.Boolean)

    # One to one
    relevant_fact_id = db.Column(db.Integer, db.ForeignKey('fact.id'))
    relevant_fact = db.relationship('Fact', uselist=False, backref='message')

    file_request = db.relationship('FileRequest', uselist=False, backref='message')

    def request_file(self, document_type):
        self.file_request = FileRequest(document_type=document_type)


class FileRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))

    # Attributes
    document_type = db.Column(db.Enum(DocumentType), nullable=False)

    def __init__(self, document_type):
        self.document_type = document_type


class FactEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    fact_id = db.Column(db.Integer, db.ForeignKey('fact.id'))

    # Attributes
    value = db.Column(db.String(255), nullable=False)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))

    # Attributes
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


'''
----------------------
Bootstrapping Database
----------------------
'''
print("Creating database tables from models.py")
db.create_all()

print("Loading database with pre-defined fact values.")


# Function that persists a model to the db if it doesn't already exist
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance is None:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


defined_facts = [
    {'name': 'is_student', 'type': FactType.BOOLEAN},
    {'name': 'is_habitable', 'type': FactType.BOOLEAN},
    {'name': 'has_lease_expired', 'type': FactType.BOOLEAN},
    {'name': 'lease_type', 'type': FactType.TEXT}
]
for fact_dict in defined_facts:
    get_or_create(db.session, Fact, name=fact_dict['name'], type=fact_dict['type'])

print("Finished loading pre-defined fact values.")

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


class FactSchema(ma.ModelSchema):
    class Meta:
        model = Fact


class FactEntitySchema(ma.ModelSchema):
    class Meta:
        model = FactEntity


class FileSchema(ma.ModelSchema):
    class Meta:
        fields = ('name', 'type', 'timestamp')


class MessageSchema(ma.ModelSchema):
    # Enum
    sender_type = EnumField(SenderType, by_value=True)

    # One to one
    relevant_fact = ma.Nested(FactSchema)
    file_request = ma.Nested(FileRequestSchema)

    class Meta:
        model = Message


class ConversationSchema(ma.ModelSchema):
    # Enum
    person_type = EnumField(PersonType, by_value=True)
    claim_category = EnumField(ClaimCategory, by_value=True)

    # One to many
    messages = ma.Nested(MessageSchema, many=True)
    facts = ma.Nested(FactSchema, many=True)

    class Meta:
        fields = ('id', 'name', 'person_type', 'messages', 'fact_entities')
