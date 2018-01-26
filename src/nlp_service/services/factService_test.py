import unittest

from nlp_service.services import factService
from postgresql_db.models import ClaimCategory, Conversation, PersonType, db, Fact, FactType


class FactServiceTest(unittest.TestCase):
    def test_submit_claim_category(self):
        next_fact = factService.submit_claim_category(ClaimCategory.LEASE_TERMINATION)
        self.assertIsNotNone(next_fact["fact_id"])

    def test_submit_resolved_fact(self):
        conversation = Conversation(name="Bob", person_type=PersonType.TENANT,
                                    claim_category=ClaimCategory.LEASE_TERMINATION)
        db.session.add(conversation)
        db.session.commit()

        fact = Fact.query.filter_by(name="apartment_impropre").first()
        next_fact = factService.submit_resolved_fact(conversation=conversation, current_fact=fact, entity_value="true")

        self.assertIsNotNone(next_fact["fact_id"])

    def get_next_fact(self):
        next_fact = factService.get_next_fact(ClaimCategory.LEASE_TERMINATION, ["apartment_impropre"])
        self.assertIsNotNone(next_fact)

    def get_next_fact_all_resolved(self):
        all_lease_termination_facts = list(factService.fact_mapping["lease_termination"])
        next_fact = factService.get_next_fact(ClaimCategory.LEASE_TERMINATION, all_lease_termination_facts)
        self.assertIsNone(next_fact)

    def test_extract_fact_bool(self):
        intent = {'name': 'test', 'confidence': 0.90}
        entities = []

        fact_value = factService.extract_fact_by_type(FactType.BOOLEAN, intent, entities)
        self.assertTrue(fact_value == 'test')

    def test_extract_fact_money(self):
        intent = {'name': 'test', 'confidence': 0.90}
        entities = [
            {
                'start': 18,
                'end': 28,
                'text': '50 dollars',
                'value': 50.0,
                'additional_info': {'value': 50.0, 'unit': '$'},
                'entity': 'amount-of-money',
                'extractor': 'ner_duckling',
            },
        ]

        fact_value = factService.extract_fact_by_type(FactType.MONEY, intent, entities)
        self.assertTrue(fact_value == 50.0)
