import numpy as np
from util.log import Log
from sklearn.metrics import precision_recall_fscore_support


class AbstractClassifier:

    def __init__(self, data_set):
        self.data_set = data_set
        self.model = None

    def train(self):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

    def predict(self, data):
        raise NotImplementedError

    def get_weights(self):
        if self.model is not None:
            return self.model.coef_[0]
        Log.write('Please train or load the classifier first')
        return None

    def reshape_dataset(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def test(self, x_test, y_test):
        # Test
        Log.write("Testing Classifier")
        y_predict = self.model.predict(x_test)
        num_correct = np.sum(y_predict == y_test)
        (precision, recall, f1, _) = precision_recall_fscore_support(y_test, y_predict)
        Log.write('Test accuracy: {}%'.format(
            num_correct * 100.0 / len(y_test)))
        Log.write('Precision: {}'.format(precision))
        Log.write('Recall: {}'.format(recall))
        Log.write('F1: {}'.format(f1))
