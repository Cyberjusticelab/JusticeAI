import json
from web.ml_controller import MlController
from numpy.testing import assert_array_equal
import unittest
import numpy as np
from model_training.classifier.multi_output.multi_class_svm import MultiClassSVM


class TestMlController(unittest.TestCase):
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
        0: ('additional_indemnity_money', 'int'),
        1: ('declares_housing_inhabitable', 'bool'),
        2: ('declares_resiliation_is_correct', 'bool'),
        3: ('orders_expulsion', 'bool'),
        4: ('orders_immediate_execution', 'bool'),
        5: ('orders_resiliation', 'bool'),
        6: ('orders_tenant_pay_first_of_month', 'bool'),
        7: ('rejects_landlord_demand', 'bool'),
        8: ('rejects_tenant_demand', 'bool'),
        9: ('tenant_ordered_to_pay_landlord', 'int')
    }

    mock_index = {
        'facts_vector': [
            (0, 'absent', 'bool'),
            (1, 'apartment_impropre', 'bool'),
            (2, 'apartment_infestation', 'bool'),
            (3, 'asker_is_landlord', 'bool'),
            (4, 'asker_is_tenant', 'bool'),
            (5, 'bothers_others', 'bool'),
            (6, 'case_fee_reimbursement', 'int'),
            (7, 'disrespect_previous_judgement', 'bool'),
            (8, 'incorrect_facts', 'bool'),
            (9, 'landlord_inspector_fees', 'int'),
            (10, 'landlord_notifies_tenant_retake_apartment', 'bool'),
            (11, 'landlord_pays_indemnity', 'bool'),
            (12, 'landlord_prejudice_justified', 'bool'),
            (13, 'landlord_relocation_indemnity_fees', 'int'),
            (14, 'landlord_rent_change', 'bool'),
            (15, 'landlord_rent_change_doc_renseignements', 'bool'),
            (16, 'landlord_rent_change_piece_justification', 'bool'),
            (17, 'landlord_rent_change_receipts', 'bool'),
            (18, 'landlord_retakes_apartment', 'bool'),
            (19, 'landlord_retakes_apartment_indemnity', 'bool'),
            (20, 'landlord_sends_demand_regie_logement', 'bool'),
            (21, 'landlord_serious_prejudice', 'bool'),
            (22, 'lease', 'int'),
            (23, 'proof_of_late', 'bool'),
            (24, 'proof_of_revenu', 'bool'),
            (25, 'rent_increased', 'bool'),
            (26, 'tenant_bad_payment_habits', 'bool'),
            (27, 'tenant_continuous_late_payment', 'bool'),
            (28, 'tenant_damaged_rental', 'bool'),
            (29, 'tenant_dead', 'bool'),
            (30, 'tenant_declare_insalubre', 'bool'),
            (31, 'tenant_financial_problem', 'bool'),
            (32, 'tenant_group_responsability', 'bool'),
            (33, 'tenant_individual_responsability', 'bool'),
            (34, 'tenant_is_bothered', 'bool'),
            (35, 'lack_of_proof', 'bool'),
            (36, 'tenant_landlord_agreement', 'bool'),
            (37, 'tenant_lease_fixed', 'bool'),
            (38, 'tenant_lease_indeterminate', 'bool'),
            (39, 'tenant_left_without_paying', 'bool'),
            (40, 'tenant_monthly_payment', 'int'),
            (41, 'tenant_negligence', 'bool'),
            (42, 'tenant_not_request_cancel_lease', 'bool'),
            (43, 'tenant_owes_rent', 'int'),
            (44, 'tenant_refuses_retake_apartment', 'bool'),
            (45, 'tenant_rent_not_paid_less_3_weeks', 'bool'),
            (46, 'tenant_rent_not_paid_more_3_weeks', 'bool'),
            (47, 'tenant_rent_paid_before_hearing', 'bool'),
            (48, 'tenant_violence', 'bool'),
            (49, 'tenant_withold_rent_without_permission', 'bool'),
            (50, 'violent', 'bool')],
        'outcomes_vector': [
            (0, 'additional_indemnity_date', 'int'),
            (1, 'additional_indemnity_money', 'int'),
            (2, 'declares_housing_inhabitable', 'bool'),
            (3, 'declares_resiliation_is_correct', 'bool'),
            (4, 'orders_expulsion', 'bool'),
            (5, 'orders_immediate_execution', 'bool'),
            (6, 'orders_resiliation', 'bool'),
            (7, 'orders_tenant_pay_first_of_month', 'bool'),
            (8, 'rejects_landlord_demand', 'bool'),
            (9, 'rejects_tenant_demand', 'bool'),
            (10, 'tenant_ordered_to_pay_landlord', 'int'),
            (11, 'tenant_ordered_to_pay_landlord_legal_fees', 'int')
        ]}
    MlController.classifier_index = mock_classifier_index
    MlController.indexes = mock_index

    def test_fact_dict_to_vector(self):
        # Test data
        input_json = json.loads(self.test_json)

        # Execute
        result = MlController.fact_dict_to_vector(input_json['facts'])
        # Verify

        assert_array_equal(result, [0., 0., 0., 1., 0., 0., 0., 0., 48.,
                                    0., 1., 0., 0., 0., 31., 0., 0., 540.,
                                    1., 1., 0., 0., 0., 0., 0., 0., 0., 0.,
                                    0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                    674., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                    0., 0., 0.])

    def test_outcome_vector_to_dict(self):
        binary_vector = np.array([0, 1, 0, 0, 0, 1, 1, 0, 1, 0])
        MlController.classifier_labels = self.mock_classifier_index
        result = MlController.outcome_vector_to_dict(binary_vector)
        expected_dict = {
            'outcomes_vector': {
                'rejects_tenant_demand': '1',
                'orders_expulsion': '0',
                'declares_resiliation_is_correct': '0',
                'tenant_ordered_to_pay_landlord': '0',
                'orders_tenant_pay_first_of_month': '1',
                'orders_immediate_execution': '0',
                'rejects_landlord_demand': '0',
                'declares_housing_inhabitable': '1',
                'orders_resiliation': '1',
                'additional_indemnity_money': '0'
            }
        }
        self.assertEqual(expected_dict, result)

    def test_probability_vector_to_dict(self):
        probability_vector = np.array([0, 1, 0, 0, 0, 1, 1, 0, 1, 0])
        MlController.classifier_labels = self.mock_classifier_index
        result = MlController.probability_vector_to_dict(probability_vector)
        expected_dict = {
                'rejects_tenant_demand': '1',
                'orders_expulsion': '0',
                'declares_resiliation_is_correct': '0',
                'tenant_ordered_to_pay_landlord': '0',
                'orders_tenant_pay_first_of_month': '1',
                'orders_immediate_execution': '0',
                'rejects_landlord_demand': '0',
                'declares_housing_inhabitable': '1',
                'orders_resiliation': '1',
                'additional_indemnity_money': '0'
        }
        self.assertEqual(expected_dict, result)

    def test_get_ordered_weights(self):
        expected_results = {
            'additional_indemnity_money': {
                'additional_facts': [
                    'asker_is_tenant',
                    'bothers_others'
                ],
                'important_facts': [
                    'asker_is_landlord'
                ]
            }
        }

        class MockClassifierModel:
            def __init__(self):
                self.estimators_ = []

        class MockEstimator:
            def __init__(self):
                self.coef_ = np.array([[
                    -1.52808095e-05, 1.99961642e+00, 1.85962826e-04, 3.77475828e-15,
                    -3.83904518e-05, -4.15205874e-04
                ]])

        mock_classifier_labels = {
            0: ('additional_indemnity_money', 'int'),
        }

        mock_label_column_index = {
            'outcomes_vector': [
                (0, 'additional_indemnity_money', 'int'),
                (1, 'declares_housing_inhabitable', 'bool'),
                (2, 'declares_resiliation_is_correct', 'bool')
            ],
            'facts_vector': [
                (0, 'apartment_dirty', 'bool'),
                (1, 'asker_is_landlord', 'bool'),
                (2, 'asker_is_tenant', 'bool'),
                (3, 'bothers_others', 'bool'),
                (4, 'disrespect_previous_judgement', 'bool'),
                (5, 'landlord_inspector_fees', 'int')
            ]
        }

        mock_estimator = MockEstimator()
        mock_classifier_model = MockClassifierModel()
        mock_classifier_model.estimators_.append(mock_estimator)

        linear_svc = MultiClassSVM(None)
        linear_svc.model = mock_classifier_model
        linear_svc.classifier_labels = mock_classifier_labels
        linear_svc.label_column_index = mock_label_column_index

        MlController.classifier_model = linear_svc

        result = MlController.get_weighted_facts()
        self.assertEqual(result, expected_results)

    def test_get_anti_fact(self):
        anti_facts = MlController.get_anti_facts()
        self.assertTrue(isinstance(anti_facts, dict))

    def test_get_ml_statistics(self):
        result = MlController.get_ml_statistics()
        self.assertTrue(isinstance(result, dict))