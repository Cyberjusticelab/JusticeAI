import datetime
import os
from enum import Enum

from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow_enum import EnumField

import postgresql_db.database as database

app = Flask(__name__)
db = database.connect(app, 'postgres', os.environ['POSTGRES_PASSWORD'], 'postgres')
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
    summary = db.Column(db.String(50), nullable=False)
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


class UserConfirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    fact_id = db.Column(db.Integer, db.ForeignKey('fact.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))

    # Attributes
    text = db.Column(db.Text, nullable=False)


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

    # One to one
    fact_id = db.Column(db.Integer, db.ForeignKey('fact.id'))
    fact = db.relationship('Fact', uselist=False, backref='factentity')

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
    {'name': 'absent', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'apartment_impropre', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'apartment_infestation', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'asker_is_landlord', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'asker_is_tenant', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'bothers_others', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'disrespect_previous_judgement', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'incorrect_facts', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_inspector_fees', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_notifies_tenant_retake_apartment', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_pays_indemnity', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_prejudice_justified', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_relocation_indemnity_fees', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_rent_change', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_rent_change_doc_renseignements', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_rent_change_piece_justification', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_rent_change_receipts', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_retakes_apartment', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_retakes_apartment_indemnity', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_sends_demand_regie_logement', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'landlord_serious_prejudice', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'lease', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'proof_of_late', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'proof_of_revenu', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'rent_increased', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_bad_payment_habits', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_continuous_late_payment', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_damaged_rental', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_dead', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_declare_insalubre', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_financial_problem', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_group_responsability', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_individual_responsability', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_is_bothered', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'lack_of_proof', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_landlord_agreement', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_lease_fixed', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_lease_indeterminate', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_left_without_paying', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_monthly_payment', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_negligence', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_not_request_cancel_lease', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_owes_rent', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_refuses_retake_apartment', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_rent_not_paid_less_3_weeks', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_rent_not_paid_more_3_weeks', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_rent_paid_before_hearing', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_violence', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'tenant_withold_rent_without_permission', 'summary': '', 'type': FactType.BOOLEAN},
    {'name': 'violent', 'summary': '', 'type': FactType.BOOLEAN}
]
for fact_dict in defined_facts:
    get_or_create(db.session, Fact, name=fact_dict['name'], summary=fact_dict['summary'], type=fact_dict['type'])

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
    # Enum
    type = EnumField(FactType, by_value=True)

    class Meta:
        fields = ('name', 'summary', 'type')


class FactEntitySchema(ma.ModelSchema):
    # One to one
    fact = ma.Nested(FactSchema)

    class Meta:
        fields = ('value', 'fact')


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

    # One to one
    current_fact = ma.Nested(FactSchema)

    # One to many
    messages = ma.Nested(MessageSchema, many=True)
    fact_entities = ma.Nested(FactEntitySchema, many=True)

    class Meta:
        model = Conversation
