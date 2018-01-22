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
        """
        Constructor
        :param data_set: [{
            name: 'AZ-XXXXXXX.txt',
            demands_vector: [...],
            facts_vector: [...],
            outcomes_vector: [...]
        },
        {
            ...
        }]
        """
        AbstractClassifier.__init__(self, data_set)

    def train(self):
        """
        Train a classifier using Linear SVC
        1) reshape date in a format that sklearn understands
        2) Binarize data for multi output
        3) split training data
        4) train (fit)
        5) test model
        :return: None
        """
        x_total, y_total = self.reshape_dataset() # 1
        mlb = MultiLabelBinarizer() # 2
        y_total = mlb.fit_transform(y_total)

        x_train, x_test, y_train, y_test = train_test_split(
            x_total, y_total, test_size=0.20) # 3

        Log.write("Sample size: {}".format(len(x_total)))
        Log.write("Train size: {}".format(len(x_train)))
        Log.write("Test size: {}".format(len(x_test)))
        Log.write("Training Classifier Using Linear SVC")

        clf = OneVsRestClassifier(SVC()) # 4
        clf.fit(x_train, y_train)
        self.model = clf
        self.test(x_test, y_test) # 5

    def save(self):
        """
        Saves model
        :return: None
        """
        save = Save()
        save.save_binary("linear_svc_model.bin", self.model)

    def predict(self, data):
        """
        Predicts an outcome given facts
        :param data: numpy([
            [1, 0, 0, ...],
            [1, 0, 1, ...],
            ...
        ])
        :return: np.array([...])
        """
        return self.model.predict(data)

    def load(self):
        """

        :return:
        """
        self.model = Load.load_binary("linear_svc_model.bin")

    def reshape_dataset(self):
        """

        :return:
        """
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