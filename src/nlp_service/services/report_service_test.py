import unittest
from unittest.mock import Mock

from nlp_service.services import ml_service, report_service
from postgresql_db.models import db, Conversation, PersonType, Fact, FactEntity, ClaimCategory

report_service.ml_service.get_statistics = Mock(return_value={
    "data_set": {
        "size": 40000
    },
    "regressor": {
        "additional_indemnity_money": {
            "mean": 1477.7728467101024,
            "std": 1927.8147997893939,
            "variance": 3716469.9022870203
        },
        "tenant_pays_landlord": {
            "mean": 2148.867088064977,
            "std": 2129.510243010276,
            "variance": 4534813.8750856845
        }
    }
})


class ReportServiceTest(unittest.TestCase):
    def test_create_report(self):
        mock_ml_prediction = {
            "orders_resiliation": 1,
            "orders_immediate_execution": 1,
            "additional_indemnity_money": 500
        }
        mock_ml_probabilities = {
            "orders_resiliation": "0.5",
            "orders_immediate_execution": "0.5",
            "additional_indemnity_money": "0.5"
        }
        mock_ml_similar_precedents = [
            {
                "distance": 10.683943352590694,
                "facts": {
                    "apartment_dirty": False,
                    "tenant_owes_rent": "0.0",
                },
                "outcomes": {
                    "additional_indemnity_money": "0.0",
                    "orders_expulsion": False,
                    "orders_immediate_execution": False,
                    "orders_resiliation": False
                },
                "precedent": "AZ-1"
            },
            {
                "distance": 11.118096551621953,
                "facts": {
                    "apartment_dirty": False,
                    "tenant_owes_rent": "100.0"
                },
                "outcomes": {
                    "additional_indemnity_money": "50.0",
                    "orders_expulsion": False,
                    "orders_immediate_execution": True,
                    "orders_resiliation": False
                },
                "precedent": "AZ-2"
            }]

        conversation = Conversation(name="Bob", person_type=PersonType.LANDLORD,
                                    claim_category=ClaimCategory.NONPAYMENT)
        db.session.add(conversation)
        db.session.commit()

        fact = Fact.query.filter_by(name="apartment_dirty").first()
        fact_entity = FactEntity(fact=fact, value="true")
        conversation.fact_entities.append(fact_entity)
        db.session.commit()

        report = report_service.generate_report(conversation,
                                                mock_ml_prediction,
                                                mock_ml_similar_precedents,
                                                mock_ml_probabilities)

        # Accuracy
        self.assertTrue(report['accuracy'] == 0.5)

        # Curves
        self.assertTrue(report['curves']['additional_indemnity_money']['outcome_value'] == 500)

        # Data Set Size
        self.assertTrue(report['data_set'] == 40000)

        # Outcomes
        self.assertTrue("orders_resiliation" in report['outcomes'])
        self.assertTrue("orders_immediate_execution" in report['outcomes'])
        self.assertTrue("additional_indemnity_money" in report['outcomes'])
        self.assertTrue("orders_expulsion" not in report['outcomes'])
        self.assertTrue(report['outcomes']['orders_resiliation'] == True)
        self.assertTrue(report['outcomes']['additional_indemnity_money'] == 500)
        self.assertTrue(report['similar_case'] == 2)

        # Similar Precedents
        self.assertTrue(len(report['similar_precedents']) == 2)
        self.assertTrue("apartment_dirty" in report['similar_precedents'][0]["facts"])
        self.assertTrue("apartment_dirty" in report['similar_precedents'][1]["facts"])
        self.assertTrue("tenant_owes_rent" not in report['similar_precedents'][1]["facts"])
        self.assertTrue("tenant_owes_rent" not in report['similar_precedents'][1]["facts"])
        self.assertTrue("additional_indemnity_money" in report['similar_precedents'][0]["outcomes"])
        self.assertTrue("additional_indemnity_money" in report['similar_precedents'][1]["outcomes"])
        self.assertTrue("orders_expulsion" not in report['similar_precedents'][0]["outcomes"])
        self.assertTrue("orders_expulsion" not in report['similar_precedents'][1]["outcomes"])