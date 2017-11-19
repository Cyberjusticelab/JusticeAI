from sklearn import svm
from train import load_data, load_new_data
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
import numpy as np


# Prep data

print("loading data")
values = load_data()
print("loading regex data")
prec = load_new_data()
values = values[1:1000]

print("merging data")
new_val = []
for val in values:
  if val['name'] + '.txt' in prec.keys():
    new_val.append({'name': val['name'], 'facts_vector' : np.fromiter(prec[val['name'] + '.txt'].values(), dtype=np.int32), 'decisions_vector' : val['decisions_vector']})


x_total = np.array(
    [np.reshape(precedent['facts_vector'], (len(precedent['facts_vector'],))) for precedent in values])
y_total = np.array(
    [precedent['decisions_vector'][0] for precedent in values])
x_train, x_test, y_train, y_test = train_test_split(
    x_total, y_total, test_size=0.20, random_state=42)
print("Sample size: {}".format(len(x_total)))
print("Train size: {}".format(len(x_train)))
print("Test size: {}".format(len(x_test)))

print("Training Classifier")
clf = svm.SVC(kernel='linear')
clf.fit(x_train, y_train)

# Test
print("Testing Classifier")
y_predict = clf.predict(x_test)
num_correct = np.sum(y_predict == y_test)
(precision, recall, f1, _) = precision_recall_fscore_support(y_test, y_predict)
print('Test accuracy: {}%'.format(num_correct * 100.0/len(y_test)))
print('Precision: {}'.format(precision))
print('Recall: {}'.format(recall))
print('F1: {}'.format(f1))
