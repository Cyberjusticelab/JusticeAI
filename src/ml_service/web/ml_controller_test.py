import json
from web.ml_controller import MlController
from numpy.testing import assert_array_equal
import unittest
import numpy as np


class TestTrainingDriver(unittest.TestCase):
    test_json = """
    {
        "facts": {
        "absent": 0,
        "apartment_impropre": 0,
        "apartment_infestation": 0,
        "asker_is_landlord": 1,
        "asker_is_tenant": 0,
        "bothers_others": 0,
        "case_fee_reimbursement": 0,
        "disrespect_previous_judgement": 0,
        "incorrect_facts": 48,
        "landlord_inspector_fees": 0,
        "landlord_notifies_tenant_retake_apartment": 1,
        "landlord_pays_indemnity": 0,
        "landlord_prejudice_justified": 0,
        "landlord_relocation_indemnity_fees": 0,
        "landlord_rent_change": 31,
        "landlord_rent_change_doc_renseignements": 0,
        "landlord_rent_change_piece_justification": 0,
        "landlord_rent_change_receipts": 540,
        "landlord_retakes_apartment": 1,
        "landlord_retakes_apartment_indemnity": 1,
        "landlord_sends_demand_regie_logement": 0,
        "landlord_serious_prejudice": 0,
        "tenant_lease_indeterminate": 674.2
        } 
    }
    """

    def test_dict_to_int_vector(self):
        # Test data
        input_json = json.loads(self.test_json)

        # Execute
        result = MlController.dict_to_int_vector(input_json['facts'])
        print(result)
        # Verify

        assert_array_equal(result, [0., 0., 0., 1., 0., 0., 0., 0., 48.,
                                    0., 1., 0., 0., 0., 31., 0., 0., 540.,
                                    1., 1., 0., 0., 0., 0., 0., 0., 0., 0.,
                                    0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                    674., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                    0., 0., 0.])

    def test_dict_to_bool_vector(self):
        # Test data
        input_json = json.loads(self.test_json)

        # Execute
        result = MlController.dict_to_bool_vector(input_json['facts'])
        print(result)
        # Verify

        assert_array_equal(result, [0., 0., 0., 1., 0., 0., 0., 0., 1.,
                                    0., 1., 0., 0., 0., 1., 0., 0., 1.,
                                    1., 1., 0., 0., 0., 0., 0., 0., 0., 0.,
                                    0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                    1., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                    0., 0., 0.])

    def test_vector_to_dict(self):
        binary_vector = np.array([0, 1, 0, 0, 0, 1, 1, 0, 1, 0])
        integer_vector = np.array([43, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 80])
        result = MlController.vector_to_dict(binary_vector, integer_vector)
        expected_dict = {
            'outcomes_vector': {
                'additional_indemnity_money': 1,
                'rejects_tenant_demand': 0,
                'orders_immediate_execution': 1,
                'tenant_ordered_to_pay_landlord': 1,
                'additional_indemnity_date': 43,
                'orders_expulsion': 0,
                'declares_housing_inhabitable': 0,
                'orders_tenant_pay_first_of_month': 0,
                'declares_resiliation_is_correct': 0,
                'tenant_ordered_to_pay_landlord_legal_fees': 80,
                'rejects_landlord_demand': 1,
                'orders_resiliation': 1
            }
        }
        self.assertEqual(expected_dict, result)