from global_variables.global_variable import Global
from outcome_predictor.basic_neural_net import BasicNeuralNet
import os
import joblib
import pdb
import numpy as np


def load_data():
    file = open('structured_precedent.bin', 'rb')
    model = joblib.load(file)
    file.close()
    resilie = 0
    for (key, val) in model.items():
        with open(Global.precedent_directory + key + '.txt', 'r', encoding="ISO-8859-1") as f:
            isFound = False
            val['decisions_vector'] = np.array([0])
            for line in f:
                if "RÉSILIE" in line and isFound is False:
                    val['decisions_vector'] = np.array([1])
                    isFound = True
    return model

print('loading data')
model = load_data()
neuralNet = BasicNeuralNet(model)
neuralNet.train()
