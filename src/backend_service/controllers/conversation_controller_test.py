import unittest

from werkzeug.exceptions import HTTPException

from backend_service.app import app
from backend_service.controllers import conversation_controller
from postgresql_db.models import *



class ConversationControllerTest(unittest.TestCase):
    def test_get_conversation(self):
        with app.test_request_context():
            conversation = Conversation(name="Bob", person_type=PersonType.TENANT,
                                        claim_category=ClaimCategory.LEASE_TERMINATION)
            db.session.add(conversation)
            db.session.commit()

            conversation_json = conversation_controller.get_conversation(conversation.id)
            self.assertIsNotNone(conversation_json)

    def test_get_conversation_error(self):
        with app.test_request_context():
            with self.assertRaises(HTTPException):
                conversation_json = conversation_controller.get_conversation(100)

    def test_init_conversation(self):
        with app.test_request_context():
            init_response = conversation_controller.init_conversation("Bob", "tenant")
            self.assertIsNotNone(init_response)

    def test_init_conversation_error(self):
        with app.test_request_context():
            with self.assertRaises(HTTPException):
                init_response = conversation_controller.init_conversation("Bob", "bad_person_type")

    def test_get_fact_entities(self):
        with app.test_request_context():
            conversation = Conversation(name="Bob", person_type=PersonType.TENANT,
                                        claim_category=ClaimCategory.LEASE_TERMINATION)
            db.session.add(conversation)
            db.session.commit()

            fact = Fact.query.filter_by(name="apartment_impropre").first()
            fact_entity = FactEntity(fact=fact, value="true")
            conversation.fact_entities.append(fact_entity)
            db.session.commit()

            fact_entities_json = conversation_controller.get_fact_entities(conversation.id)
            self.assertIsNotNone(fact_entities_json)

    def test_delete_fact_entities(self):
        with app.test_request_context():
            conversation = Conversation(name="Bob", person_type=PersonType.TENANT,
                                        claim_category=ClaimCategory.LEASE_TERMINATION)
            db.session.add(conversation)
            db.session.commit()

            fact = Fact.query.filter_by(name="apartment_impropre").first()
            fact_entity = FactEntity(fact=fact, value="true")
            conversation.fact_entities.append(fact_entity)
            db.session.commit()

            delete_fact_entity_json = conversation_controller.delete_fact_entity(conversation.id, fact_entity.id)
            self.assertIsNotNone(delete_fact_entity_json)
            self.assertTrue(fact_entity not in conversation.fact_entities)

    def test_delete_fact_entities_non_existent(self):
        with app.test_request_context():
            conversation = Conversation(name="Bob", person_type=PersonType.TENANT,
                                        claim_category=ClaimCategory.LEASE_TERMINATION)
            db.session.add(conversation)
            db.session.commit()

            with self.assertRaises(HTTPException):
                delete_fact_entity_json = conversation_controller.delete_fact_entity(conversation.id, 100)

    def test_receive_message_no_nlp(self):
        with app.test_request_context():
            conversation = Conversation(name="Bob", person_type=PersonType.TENANT,
                                        claim_category=ClaimCategory.LEASE_TERMINATION)
            db.session.add(conversation)
            db.session.commit()

            message_json = conversation_controller.receive_message(conversation.id, "")
            self.assertIsNotNone(message_json)

    def test_get_file_list(self):
        with app.test_request_context():
            conversation = Conversation(name="Bob", person_type=PersonType.TENANT,
                                        claim_category=ClaimCategory.LEASE_TERMINATION)
            db.session.add(conversation)
            db.session.commit()

            file_list_json = conversation_controller.get_file_list(conversation.id)
            self.assertIsNotNone(file_list_json)
