import unittest

import numpy as np

from model_training.regression.multi_output.multi_output_regression import MultiOutputRegression


class TestMultiOutputRegression(unittest.TestCase):
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
        9: ('tenant_ordered_to_pay_landlord', 'int'),
        10: ('additional_indemnity_date', 'int'),
        11: ('tenant_ordered_to_pay_landlord_legal_fees', 'int')
    }

    mock_facts = [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1]
    mock_outcomes = np.array([1, 0, 1, 1, 0, 1, 0, 0, 0, 0])

    def test_predict(self):
        regression_model = MultiOutputRegression()
        regression_model.months_unpaid_index = 1
        regression_model.monthly_payment_index = 1
        outcomes = regression_model.predict(self.mock_facts, self.mock_outcomes)
        for i in range(len(outcomes)):
            self.assertEqual(self.mock_outcomes[i], outcomes[i])
