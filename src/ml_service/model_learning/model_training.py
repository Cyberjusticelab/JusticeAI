import numpy as np

from model_learning.neural_net import neural_net
from util.log import Log
from util.file import Load

def run (action="lease_termination"):
    Log.write("Running model learning")
    if action=="lease_termination":
        resiliation_custers = [1, 2, 12, 17, 23, 25, 63, 78, 84, 96, 97, 98, 119, 138, 140, 143, 190, 197, 199, 253,
                            284, 306, 346, 381, 384, 393, 395, 423, 442, 445, 451, 463, 468, 506, 510, 512, 543, 560]
        # get precedent data
        precedent_data = Load.load_binary('precedent_vector.bin')
        valid_values = [precedent for precedent in precedent_data.values() if precedent[
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
        # train data
        precedent_data = valid_values
        neuralNet = neural_net.NeuralNet(precedent_data)
        neuralNet.train()
