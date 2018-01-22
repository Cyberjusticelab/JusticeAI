import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from model_training.abstract_models.abstract_classifier import AbstractClassifier
from util.file import Load, Save
from util.log import Log


class LinearSVC(AbstractClassifier):

    def __init__(self, data_set):
        AbstractClassifier.__init__(self, data_set)
        self.mlb = None

    def train(self):
        x_total, y_total = self.reshape_dataset()
        mlb = MultiLabelBinarizer()
        y_total = mlb.fit_transform(y_total)

        x_train, x_test, y_train, y_test = train_test_split(
            x_total, y_total, test_size=0.20)

        Log.write("Sample size: {}".format(len(x_total)))
        Log.write("Train size: {}".format(len(x_train)))
        Log.write("Test size: {}".format(len(x_test)))
        Log.write("Training Classifier Using Linear SVC")

        clf = OneVsRestClassifier(SVC())
        clf.fit(x_train, y_train)
        self.model = clf
        #self.test(x_test, y_test)

    def save(self):
        save = Save()
        save.save_binary("linear_svc_model.bin", self.model)

    def predict(self, data):
        return self.model.predict(data)

    def get_weights(self):
        pass

    def load(self):
        """
            Loads the classifier from its binary
        """
        self.model = Load.load_binary("linear_svc_model.bin")

    def reshape_dataset(self):
        x_total = np.array(
            [np.reshape(precedent['facts_vector'], (len(precedent['facts_vector'],))) for precedent in self.data_set])

        y_list = []
        for precedent in self.data_set:
            classified_precedent = []
            for i in range(len(precedent['outcomes_vector'])):
                if precedent['outcomes_vector'][i] == 1:
                    classified_precedent.append(i)
            y_list.append(classified_precedent)
        y_total = np.array(y_list)
        return x_total, y_total