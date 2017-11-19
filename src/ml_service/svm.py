from sklearn import svm
from train import load_data, load_new_data
from sklearn.model_selection import train_test_split
import numpy as np


# Prep data

print("loading data")
values = load_data()
print("loading regex data")
prec = load_new_data()
values = values[1:20000]

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

print('Test accuracy: {}%'.format(num_correct * 100.0/len(y_test)))
