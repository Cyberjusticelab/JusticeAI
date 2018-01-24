import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from util.file import Load, Save
from util.log import Log
from feature_extraction.post_processing.regex.regex_tagger import TagPrecedents


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

    def get_weights(self):
        """
        The weight associated with each input fact.
        Useful in seeing which facts the classifier
        values more than others
        :return: None
        """
        if self.model is not None:
            return self.model.coef_[0]
        Log.write('Please train or load the classifier first')
        return None

    def __test(self, x_test, y_test):
        """

        :param x_test:
        :param y_test:
        :return: None
        """
        indices = TagPrecedents().get_intent_indice()['outcomes_vector']
        Log.write("Testing Classifier")
        y_predict = self.model.predict(x_test)
        Log.write("Classifier results:\n")
        for i in range(len(y_predict[0])):
            yp = y_predict[:, [i]]
            yt = y_test[:, [i]]
            num_correct = np.sum(yp == yt)
            (precision, recall, f1, _) = precision_recall_fscore_support(yt, yp)
            Log.write('Column: {}'.format(indices[self.mlb.classes_[i]][1]))
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
        indices = TagPrecedents().get_intent_indice()['outcomes_vector']
        for i in range(len(self.mlb.classes_)):
            linear_labels[i] = indices[self.mlb.classes_[i]][1]
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
        return self.model.predict([data])

    def load(self):
        """
        Returns a model of the classifier
        :return: OneVsRestClassifier(SVC())
        """
        self.model = Load.load_binary("multi_class_svm_model.bin")

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
            2.1) The data looks as such: [1, 1, 1, 0, 1, 0, 0, 1...]

            2.2) We must create a new list with only the index of the columns where
                 there are values of '1'. This is necessary because the sklearn
                 algorithm expects this kind of input.

            2.3) Example:        (transformation)
                [1, 1, 0, 0, 1] ------------------> [0, 1, 4]

            2.4) Create a 2D numpy array from the new list:[
                [precedent #1 outcomes],
                [precedent #2 outcomes],
                ...
            ]
        :return: x_total <#1.1>, y_total <#2.4>
        """

        # --------------------1--------------------------
        x_total = np.array(
            [np.reshape(precedent['facts_vector'], (len(precedent['facts_vector'],))) for precedent in self.data_set])

        for i in range(len(x_total)):
            for j in range(len(x_total[i])):
                if x_total[i][j] > 1:
                    x_total[i][j] = 1

        # --------------------2--------------------------
        y_list = []
        for precedent in self.data_set:
            classified_precedent = []
            for i in range(len(precedent['outcomes_vector'])):
                if precedent['outcomes_vector'][i] == 1:
                    classified_precedent.append(i)
            y_list.append(classified_precedent)
        y_total = np.array(y_list)
        return x_total, y_total