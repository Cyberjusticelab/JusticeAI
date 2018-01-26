import unittest
from model_training.regression.multi_class_svr import MultiClassSVR
import numpy as np
from util.constant import Path
import os


class TestLinearSvc(unittest.TestCase):
    precedent1 = {'facts_vector': [550, 0, 0, 0], 'outcomes_vector': [500, 1, 0]}
    precedent2 = {'facts_vector': [292, 1, 0, 0], 'outcomes_vector': [254, 1, 0]}
    precedent3 = {'facts_vector': [800, 1, 0, 0], 'outcomes_vector': [847, 0, 0]}
    precedent4 = {'facts_vector': [30, 0, 1, 0], 'outcomes_vector': [28, 1, 1]}
    precedent5 = {'facts_vector': [440, 0, 1, 0], 'outcomes_vector': [445, 1, 0]}
    precedent6 = {'facts_vector': [110, 1, 1, 0], 'outcomes_vector': [120, 1, 0]}
    precedent7 = {'facts_vector': [5, 1, 1, 0], 'outcomes_vector': [4, 0, 0]}
    precedent8 = {'facts_vector': [600, 0, 0, 1], 'outcomes_vector': [592.1, 1, 0]}

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
        linear_svc = MultiClassSVR(self.data)
        linear_svc.train()
        data = np.array([550, 0, 0, 0])
        expected_result = [500, 0, 0]
        predicted_result = linear_svc.predict(data)[0]
        for i in range(len(predicted_result)):
            self.assertGreaterEqual(expected_result[i] + (expected_result[i] * 0.1), predicted_result[i])
            self.assertLessEqual(expected_result[i] - (expected_result[i] * 0.1), predicted_result[i])

    def test_reshape_dataset(self):
        linear_svc = MultiClassSVR(self.data)
        x, y = linear_svc.reshape_dataset()
        x = x[0]
        y = y[0]

        expected_x =[
            [550, 0, 0, 0],
            [292, 1, 0, 0],
            [800, 1, 0, 0],
            [30, 0, 1, 0],
            [440, 0, 1, 0],
            [110, 1, 1, 0],
            [5, 1, 1, 0],
            [600, 0, 0, 1]
        ]

        expected_y = [
            [500, 0, 0],
            [254, 0, 0],
            [847, 0, 0],
            [28, 0, 0],
            [445, 0, 0],
            [120, 0, 0],
            [4, 0, 0],
            [592.1, 0, 0]
        ]

        for i in range(len(x)):
            self.assertEqual(x[i], expected_x[0][i])

        for i in range(len(y)):
            self.assertEqual(y[i], expected_y[0][i])

    def test_get_weights(self):
        linear_svc = MultiClassSVR(self.data)

    def test_evaluate_best_parameters(self):
        linear_svr = MultiClassSVR(self.data)
        results = linear_svr.evaluate_best_parameters()
        self.assertTrue(type(results) == list)
        self.assertTrue(type(results[0]) == dict)
