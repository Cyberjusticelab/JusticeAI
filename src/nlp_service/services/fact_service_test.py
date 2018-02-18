import unittest
from unittest.mock import Mock

from nlp_service.services import fact_service
from postgresql_db.models import ClaimCategory, Conversation, PersonType, db, Fact, FactType, FactEntity

fact_service.ml_service.get_anti_facts = Mock(return_value={
    "not_violent": "violent",
    "tenant_individual_responsability": "tenant_group_responsability",
    "tenant_lease_fixed": "tenant_lease_indeterminate",
    "tenant_rent_not_paid_less_3_weeks": "tenant_rent_not_paid_more_3_weeks"
})

fact_service.ml_service.get_outcome_facts = Mock(return_value={
    "orders_resiliation": {
        "important_facts": [
            "tenant_rent_not_paid_more_3_weeks",
            "bothers_others",
            "disrespect_previous_judgement"
        ],
        "additional_facts": [
            "asker_is_landlord",
            "rent_increased",
            "tenant_monthly_payment",
            "tenant_financial_problem"
        ]
    }
})


class FactServiceTest(unittest.TestCase):
    def test_submit_claim_category(self):
        conversation = Conversation(name="Bob", person_type=PersonType.TENANT,
                                    claim_category=ClaimCategory.LEASE_TERMINATION)
        db.session.add(conversation)
        db.session.commit()

        next_fact = fact_service.submit_claim_category(conversation)
        self.assertIsNotNone(next_fact["fact_id"])

    def test_submit_resolved_fact(self):
        conversation = Conversation(name="Bob", person_type=PersonType.TENANT,
                                    claim_category=ClaimCategory.LEASE_TERMINATION)
        db.session.add(conversation)
        db.session.commit()

        fact = Fact.query.filter_by(name="apartment_dirty").first()
        next_fact = fact_service.submit_resolved_fact(conversation=conversation, current_fact=fact, entity_value="true")

        self.assertIsNotNone(next_fact["fact_id"])

    def test_get_next_fact(self):
        conversation = Conversation(name="Bob", person_type=PersonType.TENANT,
                                    claim_category=ClaimCategory.LEASE_TERMINATION)
        db.session.add(conversation)
        db.session.commit()

        next_fact = fact_service.get_next_fact(conversation)
        self.assertIsNotNone(next_fact)

    def test_get_next_fact_all_resolved(self):
        all_lease_termination_facts = fact_service.get_category_fact_list("lease_termination")

        # Concat all the facts
        all_facts = []
        all_facts.extend(all_lease_termination_facts["facts"])
        all_facts.extend(all_lease_termination_facts["additional_facts"])

        # Define a conversation
        conversation = Conversation(name="Bob", person_type=PersonType.TENANT,
                                    claim_category=ClaimCategory.LEASE_TERMINATION)

        # Add all facts to the conversation as resolved
        for fact_key in all_facts:
            fact = Fact.query.filter_by(name=fact_key).first()
            fact_entity = FactEntity(fact=fact, value="false")
            conversation.fact_entities.append(fact_entity)

        db.session.add(conversation)
        db.session.commit()

        next_fact = fact_service.get_next_fact(conversation)
        self.assertIsNone(next_fact)

    def test_replace_anti_facts(self):
        anti_fact_dict = {
            "not_violent": "violent",
            "tenant_individual_responsability": "tenant_group_responsability",
            "tenant_lease_fixed": "tenant_lease_indeterminate",
            "tenant_rent_not_paid_less_3_weeks": "tenant_rent_not_paid_more_3_weeks"
        }

        fact_list = ["not_violent", "tenant_lease_indeterminate", "tenant_rent_not_paid_more_3_weeks"]
        expected_fact_list = ["violent", "tenant_lease_fixed", "tenant_rent_not_paid_more_3_weeks"]

        processed_fact_list = fact_service.replace_anti_facts(fact_list, anti_fact_dict)

        self.assertListEqual(processed_fact_list, expected_fact_list)

    def test_extract_fact_bool(self):
        intent = {'name': 'true', 'confidence': 0.90}
        entities = []

        fact_value = fact_service.extract_fact_by_type(FactType.BOOLEAN, intent, entities)
        self.assertTrue(fact_value == 'true')

    def test_extract_fact_money(self):
        intent = {'name': 'true', 'confidence': 0.90}
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

        fact_value = fact_service.extract_fact_by_type(FactType.MONEY, intent, entities)
        self.assertTrue(fact_value == 50.0)
