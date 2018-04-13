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
        predicted_result = linear_svc.predict(data)[0][0]
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
                    'asker_is_tenant',
                    'bothers_others'
                ],
                'important_facts': [
                    'asker_is_landlord',
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

        result = linear_svc.get_ordered_weights()
        self.assertEqual(result, expected_results)
