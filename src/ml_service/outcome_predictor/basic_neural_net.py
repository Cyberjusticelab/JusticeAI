from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from global_variables.global_variable import Global
from sklearn.model_selection import train_test_split
import numpy as np
import joblib


class BasicNeuralNet(object):

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def train(self):
        """
            Trains the neural network.
            Current config: Input -> 64 Nodes -> Outputs
        """
        vals = self.dictionary.values()
        vals = [precedent for precedent in self.dictionary.values() if precedent[
            'facts_vector'] is not None]

        # Prep data
        print('splitting data')
        x_total = np.array(
            [np.reshape(precedent['facts_vector'], (len(precedent['facts_vector']),)) for precedent in vals])
        y_total = np.array(
            [np.reshape(precedent['decisions_vector'], (len(precedent['decisions_vector']),)) for precedent in vals])
        y_total = to_categorical(y_total)
        x_train, x_test, y_train, y_test = train_test_split(
            x_total, y_total, test_size=0.20, random_state=42)

        # Setup Model
        print('Creating model')
        model = Sequential()
        model.add(Dense(units=64, activation='relu',
                        input_dim=len(x_total[0])))
        model.add(
            Dense(units=len(y_total[0]), activation='softmax'))
        model.compile(loss='categorical_crossentropy',
                      optimizer='sgd',
                      metrics=['accuracy'])
        # Train
        print('Starting training')
        model.fit(x_train, y_train, epochs=5, batch_size=32)

        # Test
        print('Starting testing')
        score = model.evaluate(x_test, y_test, batch_size=128)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])
        self.model = model
        self.score = score
