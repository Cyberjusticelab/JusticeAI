import joblib
import numpy as np

from model.basic_neural_net import BasicNeuralNet

# I ran a crude regex to see which clusters have resiliation
resiliation_custers = [1,
                       2,
                       12,
                       17,
                       23,
                       25,
                       63,
                       78,
                       84,
                       96,
                       97,
                       98,
                       119,
                       138,
                       140,
                       143,
                       190,
                       197,
                       199,
                       253,
                       284,
                       306,
                       346,
                       381,
                       384,
                       393,
                       395,
                       423,
                       442,
                       445,
                       451,
                       463,
                       468,
                       506,
                       510,
                       512,
                       543,
                       560
                       ]


def load_data():
    file = open('structured_precedent.bin', 'rb')
    model = joblib.load(file)
    file.close()
    valid_values = [precedent for precedent in model.values() if precedent[
        'facts_vector'] is not None and precedent['decisions_vector'] is not None]
    for val in valid_values:
        if 'decisions' in val.keys():
            del val['decisions']
        if 'facts' in val.keys():
            del val['facts']
        resiliation_values = [val['decisions_vector'][x]
                              for x in resiliation_custers]
        if np.sum(resiliation_values) > 0:
            val['decisions_vector'] = np.array([1])
        else:
            val['decisions_vector'] = np.array([0])
    return valid_values

print('loading data')
precedent_data = load_data()
neuralNet = BasicNeuralNet(precedent_data)
neuralNet.train()
