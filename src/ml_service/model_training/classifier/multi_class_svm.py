import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from util.file import Load, Save
from util.log import Log
from feature_extraction.post_processing.regex.regex_tagger import TagPrecedents
from sklearn.preprocessing import binarize
import csv


class MultiClassSVM:

    def __init__(self, data_set=None):
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
        self.data_set = data_set
        self.model = None
        self.mlb = None
        self.classifier_labels = None

    def display_weights(self):
        """
        Writes all the weights to .csv format
        1) get the facts
        2) for every outcome write the weights
        :return: None
        """
        try:
            if self.model is None:
                self.model = Load.load_binary('multi_class_svm_model.bin')
                self.classifier_labels = Load.load_binary('classifier_labels.bin')
        except:
            return None

        index = TagPrecedents().get_intent_index()
        fact_header = [" "]
        for header in index['facts_vector']:
            fact_header.append(header[1])

        with open('weights.csv', 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(fact_header)

            for i in range(len(self.model.estimators_)):
                outcome_list = [self.classifier_labels[i]]
                estimator = self.model.estimators_[i]
                weights = estimator.coef_[0]
                for j in range(len(weights)):
                    outcome_list.append(weights[j])
                writer.writerow(outcome_list)

        Log.write('Weights saved to .csv')

    def __test(self, x_test, y_test):
        """

        :param x_test:
        :param y_test:
        :return: None
        """
        index = TagPrecedents().get_intent_index()['outcomes_vector']
        Log.write("Testing Classifier")
        y_predict = self.model.predict(x_test)
        Log.write("Classifier results:\n")
        for i in range(len(y_predict[0])):
            yp = y_predict[:, [i]]
            yt = y_test[:, [i]]
            num_correct = np.sum(yp == yt)
            (precision, recall, f1, _) = precision_recall_fscore_support(yt, yp)
            Log.write('Column: {}'.format(index[self.mlb.classes_[i]][1]))
            Log.write('Test accuracy: {}%'.format(
                num_correct * 100.0 / len(yt)))
            Log.write('Precision: {}'.format(precision))
            Log.write('Recall: {}'.format(recall))
            Log.write('F1: {}\n'.format(f1))

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
        self.mlb = MultiLabelBinarizer() # 2
        y_total = self.mlb.fit_transform(y_total)

        x_train, x_test, y_train, y_test = train_test_split(
            x_total, y_total, test_size=0.20, random_state=42) # 3

        Log.write("Sample size: {}".format(len(x_total)))
        Log.write("Train size: {}".format(len(x_train)))
        Log.write("Test size: {}".format(len(x_test)))
        Log.write("Training Classifier Using Multi Class SVM")

        clf = OneVsRestClassifier(SVC(kernel='linear', random_state=42)) # 4
        clf.fit(x_train, y_train)
        self.model = clf
        self.__test(x_test, y_test) # 5

    def save(self):
        """
        Since the regression and classifier models are separate,
        then new index will be assigned to each model.

        1) Save classifier of each column into a binary format
        2) Save the prediction model into binary
        :return:
        """
        # ------------------- 1 -----------------------------
        linear_labels = {}
        indices = TagPrecedents().get_intent_index()['outcomes_vector']
        for i in range(len(self.mlb.classes_)):
            label = indices[self.mlb.classes_[i]][1]
            data_type = indices[self.mlb.classes_[i]][2]
            linear_labels[i] = label, data_type
        save = Save()
        save.save_binary("classifier_labels.bin", linear_labels)

        # ------------------- 2 -----------------------------
        save.save_binary("multi_class_svm_model.bin", self.model)

    def predict(self, data):
        """
        Predicts an outcome given facts
        :param data: numpy([1, 0, 0, ...])
        :return: np.array([...])
        """
        if self.model is None:
            self.model = Load.load_binary("multi_class_svm_model.bin")
        if self.classifier_labels is None:
            Load.load_binary('classifier_labels.bin')
        data = binarize([data], threshold=0)
        return self.model.predict(data)

    def load_classifier_labels(self):
        """
        The prediction given by the model gives a matrix with less dimensions
        then the total outcomes. The reason being that only boolean outcomes
        are kept in the prediction. We therefore have to relabel the columns.

        :return: Dict of classifier labels
            dict:{
                "column 1": <int>,
                "column 2": <int>,
                ...
             }
        """
        return Load.load_binary('classifier_labels.bin')

    def reshape_dataset(self):
        """
        Restructure the data to accomodate the sklearn library
        1) Reshape the x data
            1.1) 2D numpy array: [
                    [precedent #1 facts],
                    [precedent #2 facts],
                    ...
                ]
        2) Reshape the y data
        :return: x_total <#1.1>, y_total <#2.4>
        """

        # 1
        x_total = np.array(
            [np.reshape(precedent['facts_vector'], (len(precedent['facts_vector'],))) for precedent in self.data_set])
        x_total = binarize(x_total, threshold=0)

        # 2
        y_list = []
        for precedent in self.data_set:
            y_list.append(self.__classify_precedent(precedent))
        y_total = np.array(y_list)
        return x_total, y_total

    def __classify_precedent(self, precedent):
        """
        1) The data looks as such: [1, 1, 1, 0, 1, 0, 0, 1...]

        2) We must create a new list with only the index of the columns where
             there are values of '1'. This is necessary because the sklearn
             algorithm expects this kind of input.

        3) Example:        (transformation)
            [1, 1, 0, 0, 1] ------------------> [0, 1, 4]

        4) Create a 2D numpy array from the new list:[
            [precedent #1 outcomes],
            [precedent #2 outcomes],
            ...
            ]
        :param precedent:
            dict{
                'facts_vector': [],
                'outcomes_vector': [],
                'demands_vector': []
            }
        :return: np.array([0, 1, 4, ...])
        """
        classified_precedent = []
        outcome_vector = precedent['outcomes_vector']
        for i in range(len(outcome_vector)):
            if outcome_vector[i] >= 1:
                classified_precedent.append(i)
        return classified_precedent
