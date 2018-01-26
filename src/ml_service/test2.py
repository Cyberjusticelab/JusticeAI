import joblib
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import precision_recall_fscore_support


prec = joblib.load('/home/arekmano/workspace/JusticeAI/src/ml_service/data/binary/precedent_vectors.bin')
aa = [prece for prece in prec.values() if (prece['demands_vector'][2] > 0 or prece['demands_vector'][11] > 0)]

print("Size of dataset: %d" % (len(aa)))
# load dataset
# split into input (X) and output (Y) variables
X = np.array([a['facts_vector'] for a in aa])
Y = np.array([a['outcomes_vector'][10] > 0.1 for a in aa])


scaler = StandardScaler()

X = scaler.fit_transform(X)

print("Transform Done")

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=42)
print("Sample size: {}".format(len(X)))
print("Train size: {}".format(len(x_train)))
print("Test size: {}".format(len(x_test)))

print("Training Classifier using SVC")
clf = svm.SVC(kernel='rbf', C=7, random_state=42)
clf.fit(x_train, y_train)

# Test
print("Testing Classifier")
y_predict = clf.predict(x_test)
num_correct = np.sum(y_predict == y_test)
(precision, recall, f1, _) = precision_recall_fscore_support(y_test, y_predict)
print('Test accuracy: {}%'.format(
    num_correct * 100.0 / len(y_test)))
print('Precision: {}'.format(precision))
print('Recall: {}'.format(recall))
print('F1: {}'.format(f1))


# parameters = {'C': [5,6,7,8,9,10]}

# svc = svm.SVC(kernel='rbf')
# clf = GridSearchCV(svc, parameters)
# clf.fit(x_train, y_train)
# print(clf.best_params_)