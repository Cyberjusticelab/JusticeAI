import numpy as npr
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
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
        UPDATE
        :param x_test:
        :param y_test:
        :return: None
        """
        pass

    def train(self):
        """
        CHANGE
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
        CHANGE
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
        CHANGE THIS
        """
        self.model = Load.load_binary("multi_class_svm_model.bin")

    def reshape_dataset(self):
        """
        CHANGE THIS
        """

        # --------------------1--------------------------
        x_total = np.array(
            [np.reshape(precedent['facts_vector'], (len(precedent['facts_vector'],))) for precedent in self.data_set])

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