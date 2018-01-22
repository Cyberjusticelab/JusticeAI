import unittest
from model_training.svm.linear_svc import LinearSVC
import numpy as np


class TestLinearSvc(unittest.TestCase):
    precedent1 = {'facts_vector': [1, 0, 0, 0], 'outcomes_vector': [0, 1, 0]}
    precedent2 = {'facts_vector': [0, 1, 0, 0], 'outcomes_vector': [0, 1, 0]}
    precedent3 = {'facts_vector': [1, 1, 0, 0], 'outcomes_vector': [1, 0, 0]}
    precedent4 = {'facts_vector': [0, 0, 1, 0], 'outcomes_vector': [1, 1, 1]}
    precedent5 = {'facts_vector': [1, 0, 1, 0], 'outcomes_vector': [0, 1, 0]}
    precedent6 = {'facts_vector': [0, 1, 1, 0], 'outcomes_vector': [1, 1, 0]}
    precedent7 = {'facts_vector': [1, 1, 1, 0], 'outcomes_vector': [1, 0, 0]}
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
        linear_svc = LinearSVC(self.data)
        linear_svc.train()
        data = np.array([[1, 0, 0, 0]])
        expected_result = np.array([0, 1, 0])
        predicted_result = linear_svc.predict(data)[0]
        for i in range(len(expected_result)):
            print(expected_result[i])
            self.assertEqual(expected_result[i], predicted_result[i])

    def test_reshape_dataset(self):
        linear_svc = LinearSVC(self.data)
        x, y = linear_svc.reshape_dataset()
        x = x[0]
        y = y[0]

        expected_x =[
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
