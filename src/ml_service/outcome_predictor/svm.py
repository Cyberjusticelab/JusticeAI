from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
import numpy as np


class LinearSVM:

    def __init__(self, values):
        """
            LinearSVM constructor
            param: values: entire dataset that the classifier
                           will user to train
        """
        self.values = values

    def train(self):
        """
            Trains the Linear Support Vector Machine.
        """
        x_total = np.array(
            [np.reshape(precedent['facts_vector'], (len(precedent['facts_vector'],))) for precedent in self.values])
        y_total = np.array(
            [precedent['decisions_vector'][0] for precedent in self.values])
        x_train, x_test, y_train, y_test = train_test_split(
            x_total, y_total, test_size=0.20, random_state=42)
        print("Sample size: {}".format(len(x_total)))
        print("Train size: {}".format(len(x_train)))
        print("Test size: {}".format(len(x_test)))

        print("Training Classifier")
        clf = svm.SVC(kernel='linear')
        clf.fit(x_train, y_train)

        # Test
        print("Testing Classifier")
        y_predict = clf.predict(x_test)
        num_correct = np.sum(y_predict == y_test)
        (precision, recall, f1, _) = precision_recall_fscore_support(y_test, y_predict)
        print('Test accuracy: {}%'.format(num_correct * 100.0/len(y_test)))
        print('Precision: {}'.format(precision))
        print('Recall: {}'.format(recall))
        print('F1: {}'.format(f1))

        self.model = clf


    def predict(self, facts_vector):
        """
          Predicts the outcome, based on the given
          fact vector
          param: facts_vector: a vector representation of all the
                               facts
          returns: the predicted outcome vector
        """
        if hasattr(self, 'model'):
            return self.model.predict(facts_vector)
        print('Please train the classifier first')
        return None

    def get_weights(self):
        """
            returns: the weight associated with each input fact.
                     Useful in seeing which facts the classifier
                     values more than others
        """
        if hasattr(self, 'model'):
            return self.model.coef_[0]
        print('Please train the classifier first')
        return None
