import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC as LinSVC
from sklearn.model_selection import train_test_split
from model_training.abstract_models.abstract_classifier import AbstractClassifier
from util.file import Load, Save
from util.log import Log


class LinearSVC(AbstractClassifier):

    def __init__(self, data_set):
        AbstractClassifier.__init__(self, data_set)

    def train(self):
        x_total, y_total = self.reshape_dataset()
        x_train, x_test, y_train, y_test = train_test_split(
            x_total, y_total, test_size=0.20, random_state=42)

        Log.write("Sample size: {}".format(len(x_total)))
        Log.write("Train size: {}".format(len(x_train)))
        Log.write("Test size: {}".format(len(x_test)))
        Log.write("Training Classifier Using Linear SVC")

        mlb = MultiLabelBinarizer(sparse_output=True)
        y_train_mlb = mlb.fit_transform(y_train)

        clf = OneVsRestClassifier(LinSVC())
        clf.fit(x_train, y_train_mlb)
        self.model = clf
        self.test(x_test, y_test)
        save = Save()
        save.save_binary("linear_svc_model.bin", self.model)

    def predict(self):
        mlb = MultiLabelBinarizer(sparse_output=True)
        print(mlb.inverse_transform(self.model.predict(np.array([[0, 1, 0]]))))

    def get_weights(self):
        pass

    def load(self):
        """
            Loads the classifier from its binary
        """
        self.model = Load.load_binary("linear_svc_model.bin")

    def reshape_dataset(self):
        """
            Reshapes the given dataset to acommodate
            ML algorithm.

            x_total = m X n then y_total = x X 1

            returns: (m X n matrix, m X 1 matrix)
        """
        x_total = np.array(
            [np.reshape(precedent['facts_vector'], (len(precedent['facts_vector'],))) for precedent in self.data_set])
        y_total = np.array(
            [precedent['outcomes_vector'] for precedent in self.data_set])
        return x_total, y_total