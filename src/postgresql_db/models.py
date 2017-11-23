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
    {'name': 'absent', 'type': FactType.BOOLEAN},
    {'name': 'apartment_impropre', 'type': FactType.BOOLEAN},
    {'name': 'apartment_infestation', 'type': FactType.BOOLEAN},
    {'name': 'asker_is_landlord', 'type': FactType.BOOLEAN},
    {'name': 'asker_is_tenant', 'type': FactType.BOOLEAN},
    {'name': 'bothers_others', 'type': FactType.BOOLEAN},
    {'name': 'disrespect_previous_judgement', 'type': FactType.BOOLEAN},
    {'name': 'incorrect_facts', 'type': FactType.BOOLEAN},
    {'name': 'landlord_inspector_fees', 'type': FactType.BOOLEAN},
    {'name': 'landlord_notifies_tenant_retake_apartment', 'type': FactType.BOOLEAN},
    {'name': 'landlord_pays_indemnity', 'type': FactType.BOOLEAN},
    {'name': 'landlord_prejudice_justified', 'type': FactType.BOOLEAN},
    {'name': 'landlord_relocation_indemnity_fees', 'type': FactType.BOOLEAN},
    {'name': 'landlord_rent_change', 'type': FactType.BOOLEAN},
    {'name': 'landlord_rent_change_doc_renseignements', 'type': FactType.BOOLEAN},
    {'name': 'landlord_rent_change_piece_justification', 'type': FactType.BOOLEAN},
    {'name': 'landlord_rent_change_receipts', 'type': FactType.BOOLEAN},
    {'name': 'landlord_retakes_apartment', 'type': FactType.BOOLEAN},
    {'name': 'landlord_retakes_apartment_indemnity', 'type': FactType.BOOLEAN},
    {'name': 'landlord_sends_demand_regie_logement', 'type': FactType.BOOLEAN},
    {'name': 'landlord_serious_prejudice', 'type': FactType.BOOLEAN},
    {'name': 'lease', 'type': FactType.BOOLEAN},
    {'name': 'proof_of_late', 'type': FactType.BOOLEAN},
    {'name': 'proof_of_revenu', 'type': FactType.BOOLEAN},
    {'name': 'rent_increased', 'type': FactType.BOOLEAN},
    {'name': 'tenant_bad_payment_habits', 'type': FactType.BOOLEAN},
    {'name': 'tenant_continuous_late_payment', 'type': FactType.BOOLEAN},
    {'name': 'tenant_damaged_rental', 'type': FactType.BOOLEAN},
    {'name': 'tenant_dead', 'type': FactType.BOOLEAN},
    {'name': 'tenant_declare_insalubre', 'type': FactType.BOOLEAN},
    {'name': 'tenant_financial_problem', 'type': FactType.BOOLEAN},
    {'name': 'tenant_group_responsability', 'type': FactType.BOOLEAN},
    {'name': 'tenant_individual_responsability', 'type': FactType.BOOLEAN},
    {'name': 'tenant_is_bothered', 'type': FactType.BOOLEAN},
    {'name': 'lack_of_proof', 'type': FactType.BOOLEAN},
    {'name': 'tenant_landlord_agreement', 'type': FactType.BOOLEAN},
    {'name': 'tenant_lease_fixed', 'type': FactType.BOOLEAN},
    {'name': 'tenant_lease_indeterminate', 'type': FactType.BOOLEAN},
    {'name': 'tenant_left_without_paying', 'type': FactType.BOOLEAN},
    {'name': 'tenant_monthly_payment', 'type': FactType.BOOLEAN},
    {'name': 'tenant_negligence', 'type': FactType.BOOLEAN},
    {'name': 'tenant_not_request_cancel_lease', 'type': FactType.BOOLEAN},
    {'name': 'tenant_owes_rent', 'type': FactType.BOOLEAN},
    {'name': 'tenant_refuses_retake_apartment', 'type': FactType.BOOLEAN},
    {'name': 'tenant_rent_not_paid_less_3_weeks', 'type': FactType.BOOLEAN},
    {'name': 'tenant_rent_not_paid_more_3_weeks', 'type': FactType.BOOLEAN},
    {'name': 'tenant_rent_paid_before_hearing', 'type': FactType.BOOLEAN},
    {'name': 'tenant_violence', 'type': FactType.BOOLEAN},
    {'name': 'tenant_withold_rent_without_permission', 'type': FactType.BOOLEAN},
    {'name': 'violent', 'type': FactType.BOOLEAN}
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
    # Enum
    type = EnumField(FactType, by_value=True)

    class Meta:
        fields = ('name', 'type')


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
