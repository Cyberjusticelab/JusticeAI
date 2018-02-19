import unittest

import numpy as np

from model_training.classifier.multi_output.multi_class_svm import MultiClassSVM


class TestLinearSvc(unittest.TestCase):
    precedent1 = {'facts_vector': [1, 0, 0, 0], 'outcomes_vector': [0, 1, 0]}
    precedent2 = {'facts_vector': [0, 1, 0, 0], 'outcomes_vector': [0, 1, 0]}
    precedent3 = {'facts_vector': [1, 1, 0, 0], 'outcomes_vector': [1, 0, 0]}
    precedent4 = {'facts_vector': [0, 0, 50, 0], 'outcomes_vector': [1, 1, 1]}
    precedent5 = {'facts_vector': [1, 0, 1, 0], 'outcomes_vector': [0, 1, 0]}
    precedent6 = {'facts_vector': [0, 30, 1, 0], 'outcomes_vector': [1, 1, 0]}
    precedent7 = {'facts_vector': [42, 1, 1, 0], 'outcomes_vector': [1, 0, 0]}
    precedent8 = {'facts_vector': [0, 0, 0, 1], 'outcomes_vector': [0, 1, 0]}

    data = [
        precedent1,
        precedent2,
        precedent3,
        precedent4,
        precedent5,
        precedent6,
        precedent7,
        precedent8
    ]

    def test_svc_train(self):
        linear_svc = MultiClassSVM(self.data)
        linear_svc.train()
        data = np.array([1, 0, 0, 0])
        expected_result = np.array([0, 1, 0])
        predicted_result = linear_svc.predict(data)[0]
        for i in range(len(expected_result)):
            print(expected_result[i])
            self.assertEqual(expected_result[i], predicted_result[i])

    def test_reshape_dataset(self):
        linear_svc = MultiClassSVM(self.data)
        x, y = linear_svc.reshape_dataset()
        x = x[0]
        y = y[0]

        expected_x = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 0],
            [1, 0, 1, 0],
            [0, 1, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 1]
        ]

        expected_y = [[1], [1], [0], [0, 1, 2], [1], [0, 1], [0], [1]]

        for i in range(len(x)):
            self.assertEqual(x[i], expected_x[0][i])

        for i in range(len(y)):
            self.assertEqual(y[i], expected_y[0][i])

    def test_get_weights(self):
        linear_svc = MultiClassSVM(self.data)
        self.assertIsNone(linear_svc.weights_to_csv())

    def test_get_ordered_weights(self):
        expected_results = {
            'additional_indemnity_money': {
                'additional_facts': [
                    'tenant_financial_problem',
                    'tenant_owes_rent',
                    'asker_is_tenant',
                    'tenant_damaged_rental',
                    'tenant_individual_responsability',
                    'signed_proof_of_rent_debt',
                    'tenant_lease_indeterminate',
                    'tenant_dead',
                    'tenant_is_bothered',
                    'bothers_others'
                ],
                'important_facts': [
                    'asker_is_landlord',
                    'tenant_withold_rent_without_permission',
                    'tenant_refuses_retake_apartment',
                    'tenant_monthly_payment',
                    'tenant_not_paid_lease_timespan'
                ]
            }
        }

        class MockClassifierModel:
            def __init__(self):
                self.estimators_ = []

        class MockEstimator:
            def __init__(self):
                self.coef_ = np.array([[
                    -1.52808095e-05,  1.99961642e+00,  1.85962826e-04,  3.77475828e-15,
                     -3.83904518e-05, -4.15205874e-04,  0.00000000e+00,  0.00000000e+00,
                     -3.71814320e-04, -1.00000000e+00,  0.00000000e+00, -1.99991520e+00,
                     -6.29465072e-04,  0.00000000e+00,  3.10807320e-05, -3.55271368e-15,
                     -1.19057931e-04,  1.74643194e-04,  1.52808094e-05,  3.33583463e-01,
                     -1.56644819e-05,  1.67203983e-04,  1.48998159e-05,  0.00000000e+00,
                      3.10807320e-05, -8.69144941e-05,  1.99902547e+00,  5.12642134e-04,
                      1.99925027e+00, -3.33189308e-01, -2.00010784e+00,  1.99961517e+00,
                     -9.08096365e-05, -1.66677277e+00,  1.00000000e+00, -6.72435223e-04
                ]])
        mock_classifier_labels = {
            0: ('additional_indemnity_money', 'int'),
        }

        mock_estimator = MockEstimator()
        mock_classifier_model = MockClassifierModel()
        mock_classifier_model.estimators_.append(mock_estimator)

        linear_svc = MultiClassSVM(None)
        linear_svc.model = mock_classifier_model
        linear_svc.classifier_labels = mock_classifier_labels

        result = linear_svc.get_ordered_weights()
        self.assertEqual(result, expected_results)
