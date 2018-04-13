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
import math


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
        self.label_column_index = None

    def weights_to_csv(self):
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
        except BaseException:
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
                try:
                    weights = estimator.coef_[0]
                    for j in range(len(weights)):
                        outcome_list.append(weights[j])
                    writer.writerow(outcome_list)
                except AttributeError:
                    pass
        Log.write('Weights saved to .csv')

    def get_ordered_weights(self):
        """
        Sort all the facts by importance for every outcome

        1) If the classifier model isn't loaded then load it
        2) Load labels of the outcomes
        3) obtain labels of every fact
        4) for every estimator append all it's fact weights
        5) sort the fact in descending order by weight
        6) do not append facts with weight of 0
        7) threshold facts by using the logarithmic power of the mean
           7.1) any number with greater or equal power of magnitude is important
           7.2) other numbers make a fact unimportant

        ** Custom list for additional_indemnity_money
        :return: {
                    'additional_indemnity_money': {
                        'important_facts': [
                            'asker_is_landlord',
                            'tenant_rent_not_paid_more_3_weeks',
                            'tenant_owes_rent',
                            'tenant_left_without_paying',
                            'not_violent'
                        ],
                        'additional_facts': [
                            ...
                        ]
                    }
                }
        """
        if self.model is None:
            self.model = Load.load_binary('multi_class_svm_model.bin')
            self.classifier_labels = Load.load_binary('classifier_labels.bin')
            self.label_column_index = TagPrecedents().get_intent_index()
        weight_dict = {}

        for i in range(len(self.model.estimators_)):
            outcome_list = []
            estimator = self.model.estimators_[i]
            try:
                weights = estimator.coef_[0]
                for j in range(len(weights)):
                    if weights[j] > 0:
                        outcome_list.append([self.label_column_index['facts_vector'][j][1], weights[j]])

                outcome_list.sort(key=lambda x: abs(x[1]), reverse=True)
                weights = [abs(x[1]) for x in outcome_list]
                mean_power = math.log10(np.mean(np.array(weights)))
                important_facts = [x[0] for x in outcome_list if math.log10(abs(x[1])) >= mean_power]
                additional_facts = [x[0] for x in outcome_list if math.log10(abs(x[1])) < mean_power]
                if self.classifier_labels[i][0] == 'additional_indemnity_money':
                    important_facts.append('tenant_monthly_payment')
                    important_facts.append('tenant_not_paid_lease_timespan')
                    if 'tenant_not_paid_lease_timespan' in additional_facts:
                        additional_facts.remove('tenant_not_paid_lease_timespan')
                    if 'tenant_monthly_payment' in additional_facts:
                        additional_facts.remove('tenant_monthly_payment')
                weight_dict[self.classifier_labels[i][0]] = {}
                weight_dict[self.classifier_labels[i][0]]['important_facts'] = important_facts
                weight_dict[self.classifier_labels[i][0]]['additional_facts'] = additional_facts
            except AttributeError:
                print('Problem with {} prediction'.format(self.classifier_labels[i][0]))
        return weight_dict

    def __test(self, x_test, y_test):
        """
        1) Tests model
        2) Save the accuracy to the model metrics binary

        model_metrics -->
        {
            'data_set':{
                'size': 5000
            },
            'regressor':{
                'regressor name':{
                    'std': 4,
                    'mean': 5,
                    'variance': 42,
                    'mean_fact_vector': [3, 1, 5, 6, 2]
                }
            },
            'classifier':{
                'classifier name':{
                    'prediction_accuracy': 0.92,
                }
            }
        }

        :param x_test: numpy array
        :param y_test: numpy array
        :return: None
        """
        model_metrics = Load.load_binary('model_metrics.bin')
        if model_metrics is None:
            model_metrics = {
                'classifier': {}
            }
        elif 'classifier' not in model_metrics:
            model_metrics['classifier'] = {}

        model_metrics['data_set'] = {
            'size': len(self.data_set)
        }

        index = TagPrecedents().get_intent_index()['outcomes_vector']
        Log.write("Testing Classifier")
        y_predict = self.model.predict(x_test)
        Log.write("Classifier results:\n")
        for i in range(len(y_predict[0])):
            yp = y_predict[:, [i]]
            yt = y_test[:, [i]]
            accuracy = np.sum(yp == yt) * 100.0 / len(yt)
            column_name = index[self.mlb.classes_[i]][1]
            (precision, recall, f1, _) = precision_recall_fscore_support(yt, yp)
            Log.write('Column: {}'.format(column_name))
            Log.write('Test accuracy: {}%'.format(accuracy))
            Log.write('Precision: {}'.format(precision))
            Log.write('Recall: {}'.format(recall))
            Log.write('F1: {}\n'.format(f1))

            model_metrics['classifier'][column_name] = {
                'prediction_accuracy': accuracy,
            }
        Save().save_binary('model_metrics.bin', model_metrics)

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
        x_total, y_total = self.reshape_dataset()  # 1
        self.mlb = MultiLabelBinarizer()  # 2
        y_total = self.mlb.fit_transform(y_total)

        x_train, x_test, y_train, y_test = train_test_split(
            x_total, y_total, test_size=0.20, random_state=42)  # 3

        Log.write("Sample size: {}".format(len(x_total)))
        Log.write("Train size: {}".format(len(x_train)))
        Log.write("Test size: {}".format(len(x_test)))
        Log.write("Training Classifier Using Multi Class SVM")

        clf = OneVsRestClassifier(SVC(kernel='linear', random_state=42, probability=True))  # 4
        clf.fit(x_train, y_train)
        self.model = clf
        self.__test(x_test, y_test)  # 5

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
        1) Predicts an outcome given facts
        2) Predicts probability that prediction is correct
            2.1) Range goes from [0-1] where x < 0.5 is False
            2.2) The model only returns the probability that a fact is 1
            2.3) therefore to predict that the probability that a fact is 0 we do
                 1 - x when x < 0.5

        :param data: numpy([1, 0, 0, ...])
        :return: np.array([...])
        """
        if self.model is None:
            self.model = Load.load_binary("multi_class_svm_model.bin")
        data = binarize([data], threshold=0)
        probabilities = self.model.predict_proba(data)[0]
        predictions = self.model.predict(data)
        for i in range(len(probabilities)):
            prediction = predictions[0][i]
            if prediction == 0:
                probabilities[i] = 1 - probabilities[i]
            probabilities[i] = format(probabilities[i], '.2f')
        return self.model.predict(data), probabilities

    @staticmethod
    def load_classifier_labels():
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
            [np.reshape(precedent['facts_vector'], (len(precedent['facts_vector'], ))) for precedent in self.data_set])
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

        3) Reshape the y data
           The MultiLabelBinarizer expects a series of labels for binarization.
           From all the collected labels, it finds all the unique ones in order
           to figure out how many columns are needed in the vector. From this,
           it will place 1's and 0's accordingly in the columns. For this purpose,
           we cannot create a binarized vector here but instead we return the labels
           which are true for an outcome.

            Example:        (transformation)
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
