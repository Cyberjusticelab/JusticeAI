import unittest
from unittest import mock

from nlp_service.services import ml_service
from postgresql_db.models import db, Conversation, PersonType, Fact, FactEntity


def mock_get_anti_facts():
    return {
        "tenant_rent_not_paid_more_3_weeks": "tenant_rent_not_paid_less_3_weeks"
    }


class MlServiceTest(unittest.TestCase):
    def test_extract_prediction(self):
        mock_ml_response = {
            "outcomes_vector": {
                "orders_resiliation": 1
            }
        }
        prediction_dict = ml_service.extract_prediction("lease_termination", mock_ml_response)
        self.assertTrue("orders_resiliation" in prediction_dict)

    def test_extract_prediction_bad_key(self):
        mock_ml_response = {
            "outcomes_vector": {
                "orders_resiliation": 1
            }
        }
        prediction_dict = ml_service.extract_prediction("bad_key", mock_ml_response)
        self.assertFalse(bool(prediction_dict))

    @mock.patch('ml_service.get_anti_facts', side_effect=mock_get_anti_facts)
    def test_generate_fact_dict(self, antifact_mock):
        conversation = Conversation(name="Bob", person_type=PersonType.TENANT)
        db.session.add(conversation)
        db.session.commit()

        fact1 = Fact.query.filter_by(name="apartment_dirty").first()
        fact_entity_true = FactEntity(fact=fact1, value="true")
        conversation.fact_entities.append(fact_entity_true)
        db.session.commit()

        fact2 = Fact.query.filter_by(name="tenant_rent_not_paid_more_3_weeks").first()
        fact_entity_false = FactEntity(fact=fact2, value="false")
        conversation.fact_entities.append(fact_entity_false)
        db.session.commit()

        fact3 = Fact.query.filter_by(name="tenant_owes_rent").first()
        fact_entity_money = FactEntity(fact=fact3, value="400.00")
        conversation.fact_entities.append(fact_entity_money)
        db.session.commit()

        fact_dict = ml_service.generate_fact_dict(conversation)
        self.assertTrue(len(fact_dict) != 0)
        self.assertTrue(fact_dict["apartment_dirty"] == 1)
        self.assertTrue(fact_dict["tenant_rent_not_paid_more_3_weeks"] == 0)  # Fact
        self.assertTrue(fact_dict["tenant_rent_not_paid_less_3_weeks"] == 1)  # Anti-fact
        self.assertTrue(fact_dict["tenant_owes_rent"] == 400.00)  # Money fact
