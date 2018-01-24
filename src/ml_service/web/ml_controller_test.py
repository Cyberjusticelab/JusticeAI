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
    mock_classifier_index = {
        0: 'additional_indemnity_money',
        1: 'declares_housing_inhabitable',
        2: 'declares_resiliation_is_correct',
        3: 'orders_expulsion',
        4: 'orders_immediate_execution',
        5: 'orders_resiliation',
        6: 'orders_tenant_pay_first_of_month',
        7: 'rejects_landlord_demand',
        8: 'rejects_tenant_demand',
        9: 'tenant_ordered_to_pay_landlord'
    }

    mock_index = {
        'facts_vector': [
            (0, 'absent'),
            (1, 'apartment_impropre'),
            (2, 'apartment_infestation'),
            (3, 'asker_is_landlord'),
            (4, 'asker_is_tenant'),
            (5, 'bothers_others'),
            (6, 'case_fee_reimbursement'),
            (7, 'disrespect_previous_judgement'),
            (8, 'incorrect_facts'),
            (9, 'landlord_inspector_fees'),
            (10, 'landlord_notifies_tenant_retake_apartment'),
            (11, 'landlord_pays_indemnity'),
            (12, 'landlord_prejudice_justified'),
            (13, 'landlord_relocation_indemnity_fees'),
            (14, 'landlord_rent_change'),
            (15, 'landlord_rent_change_doc_renseignements'),
            (16, 'landlord_rent_change_piece_justification'),
            (17, 'landlord_rent_change_receipts'),
            (18, 'landlord_retakes_apartment'),
            (19, 'landlord_retakes_apartment_indemnity'),
            (20, 'landlord_sends_demand_regie_logement'),
            (21, 'landlord_serious_prejudice'),
            (22, 'lease'),
            (23, 'proof_of_late'),
            (24, 'proof_of_revenu'),
            (25, 'rent_increased'),
            (26, 'tenant_bad_payment_habits'),
            (27, 'tenant_continuous_late_payment'),
            (28, 'tenant_damaged_rental'),
            (29, 'tenant_dead'),
            (30, 'tenant_declare_insalubre'),
            (31, 'tenant_financial_problem'),
            (32, 'tenant_group_responsability'),
            (33, 'tenant_individual_responsability'),
            (34, 'tenant_is_bothered'),
            (35, 'lack_of_proof'),
            (36, 'tenant_landlord_agreement'),
            (37, 'tenant_lease_fixed'),
            (38, 'tenant_lease_indeterminate'),
            (39, 'tenant_left_without_paying'),
            (40, 'tenant_monthly_payment'),
            (41, 'tenant_negligence'),
            (42, 'tenant_not_request_cancel_lease'),
            (43, 'tenant_owes_rent'),
            (44, 'tenant_refuses_retake_apartment'),
            (45, 'tenant_rent_not_paid_less_3_weeks'),
            (46, 'tenant_rent_not_paid_more_3_weeks'),
            (47, 'tenant_rent_paid_before_hearing'),
            (48, 'tenant_violence'),
            (49, 'tenant_withold_rent_without_permission'),
            (50, 'violent')],
        'outcomes_vector': [
            (0, 'additional_indemnity_date'),
            (1, 'additional_indemnity_money'),
            (2, 'declares_housing_inhabitable'),
            (3, 'declares_resiliation_is_correct'),
            (4, 'orders_expulsion'),
            (5, 'orders_immediate_execution'),
            (6, 'orders_resiliation'),
            (7, 'orders_tenant_pay_first_of_month'),
            (8, 'rejects_landlord_demand'),
            (9, 'rejects_tenant_demand'),
            (10, 'tenant_ordered_to_pay_landlord'),
            (11, 'tenant_ordered_to_pay_landlord_legal_fees')
        ]}
    MlController.classifier_index = mock_classifier_index
    MlController.indexes = mock_index

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