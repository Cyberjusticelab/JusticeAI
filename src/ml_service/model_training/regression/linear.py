import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import explained_variance_score
from util.file import Load, Save
from util.log import Log


class LinearRegression:

    def __init__(self, data_set=None):
        self.data_set = data_set
        self.model = None

    def __test(self, x_test, y_test):
        Log.write("Testing Linear Regression")
        y_predict = self.model.predict(x_test)
        r_Score = r2_score(y_test, y_predict)
        explained_variance = explained_variance_score(y_test, y_predict)
        Log.write('R2: {}'.format(r_Score))
        Log.write('Explained Variance: {}'.format(explained_variance))

    def train(self):
        x_total, y_total = self.reshape_dataset()
        x_train, x_test, y_train, y_test = train_test_split(
            x_total, y_total, test_size=0.20, random_state=42)
        Log.write("Sample size: {}".format(len(x_total)))
        Log.write("Train size: {}".format(len(x_train)))
        Log.write("Test size: {}".format(len(x_test)))
        Log.write("Training Linear Regression")
        lrg = MultiOutputRegressor(linear_model.LinearRegression())
        lrg.fit(x_train, y_train)
        self.model = lrg
        self.__test(x_test, y_test)# 5

    def save(self):
        save = Save()
        save.save_binary("linear_regression_model.bin", self.model)

    def predict(self, data):
        return self.model.predict([data])

    def load(self):
        self.model = Load.load_binary("multi_class_svm_model.bin")

    def reshape_dataset(self):
        x_total = np.array(
            [np.reshape(precedent['facts_vector'], (len(precedent['facts_vector'],))) for precedent in self.data_set])
        y_list = []
        for precedent in self.data_set:
            filtered_precedent = []
            for i in range(len(precedent['outcomes_vector'])):
                if precedent['outcomes_vector'][i] > 1:
                    filtered_precedent.append(precedent['outcomes_vector'][i])
                else:
                    filtered_precedent.append(0)
            y_list.append(filtered_precedent)
        y_total = np.array(y_list)
        return x_total, y_total