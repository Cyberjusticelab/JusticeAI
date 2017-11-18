import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

from util.log import Log
from util.file import Save

class NeuralNet(object):

    def __init__(self, data_tuple):
        self.data_tuple = data_tuple

    def train(self):
        """
            Trains the neural network.
            Current config: Input -> 64 Nodes -> Outputs
        """
        # import pdb;pdb.set_trace()
        # Prep data
        Log.write("Starting Neural Network Training")
        x_total = np.array(
            [np.reshape(precedent["facts_vector"], (len(precedent["facts_vector"],))) for precedent in self.data_tuple])
        y_total = np.array(
            [np.reshape(precedent["decisions_vector"], (len(precedent["decisions_vector"],))) for precedent in self.data_tuple])
        y_total = to_categorical(y_total)
        x_train, x_test, y_train, y_test = train_test_split(
            x_total, y_total, test_size=0.20, random_state=42)

        # Setup neural network
        Log.write("Creating learning Model")
        nn = Sequential()
        nn.add(Dense(units=64, activation="relu",
                        input_dim=len(x_total[0])))
        nn.add(
            Dense(units=len(y_total[0]), activation="softmax"))
        nn.compile(loss="categorical_crossentropy",
                      optimizer="sgd",
                      metrics=["accuracy"])
        # Train
        Log.write("Starting training Neural Network")
        nn.fit(x_train, y_train, epochs=5, batch_size=32)

        # Test
        Log.write("Starting testing")
        score = nn.evaluate(x_test, y_test, batch_size=128)
        Log.write("Test loss:" + score[0])
        Log.write("Test accuracy:" + score[1])
        self.nn = nn
        self.score = score
        
        # Saving model
        s = Save(r"neural_network")
        s.save_binary("neural_network_model.bin", nn)
        return nn
