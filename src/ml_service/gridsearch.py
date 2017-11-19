from sklearn import svm
from sklearn.model_selection import GridSearchCV

from train import load_data
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from global_variables.global_variable import Global
from sklearn.model_selection import train_test_split
import numpy as np
import joblib

values = load_data()
values = values[1:1000]
x_total = np.array(
    [np.reshape(precedent['facts_vector'], (len(precedent['facts_vector'],))) for precedent in values])
y_total = np.array(
    [precedent['decisions_vector'][0] for precedent in values])
x_train, x_test, y_train, y_test = train_test_split(
    x_total, y_total, test_size=0.20, random_state=42)

parameters = {'kernel': ('linear', 'poly', 'sigmoid',
                         'rbf'), 'C': [1, 2, 3, 10]}

svc = svm.SVC()
clf = GridSearchCV(svc, parameters)
clf.fit(x_train, y_train)
