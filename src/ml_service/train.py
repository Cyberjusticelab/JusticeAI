from global_variables.global_variable import Global
from outcome_predictor.basic_neural_net import BasicNeuralNet
import os
import joblib
import pdb
import numpy as np


def load_data(useCached=False):
    if useCached:
        file = open('structured_precedent_updated.bin', 'rb')
        return joblib.load(file)
    file = open('structured_precedent.bin', 'rb')
    model = joblib.load(file)
    file.close()
    resilie = 0
    for (key, val) in model.items():
        with open(Global.precedent_directory + key + '.txt', 'r', encoding="ISO-8859-1") as f:
            isFound = False
            val['decisions_vector'] = np.array([0])
            del val['decisions']
            del val['facts']
            for line in f:
                if "RÉSILIE" in line and isFound is False:
                    val['decisions_vector'] = np.array([1])
                    isFound = True
    print('save update')
    joblib.dump(model, 'structured_precedent_updated.bin')
    return model

print('loading data')
model = load_data(True)
neuralNet = BasicNeuralNet(model)
neuralNet.train()
