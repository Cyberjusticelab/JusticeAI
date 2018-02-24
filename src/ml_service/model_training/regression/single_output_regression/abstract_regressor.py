from util.file import Load, Save
from util.constant import Path
from keras.models import load_model
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
import os
import numpy as np
from util.log import Log


class AbstractRegressor:

    def __init__(self, regressor_name, dataset = None, outcome_index = 0):
        """
        Constructor
        :param data_set: [{
            name: 'AZ-XXXXXXX.txt',
            demands_vector: [...],
            facts_vector: [...],
            outcomes_vector: [...]
        },
        {
            ...
        }]
        """
        self.input_dimensions = None
        self.model = None
        self.regressor_name = regressor_name
        self.mean_vector = None
        if dataset is not None:
            self.dataset = [precedent for precedent in dataset if precedent[
                'outcomes_vector'][outcome_index] > 1]
            facts_vector = [x['facts_vector'] for x in self.dataset]
            self.mean_vector = np.mean(facts_vector, axis=0)
            mean_dict = Load.load_binary('regressor_means.bin')
            mean_dict[regressor_name] = self.mean_vector
            Save().save_binary('regressor_means.bin', mean_dict)
            self.outcome_index = outcome_index
        else:
            self.load()

    def _nn_architecture(self):
        raise NotImplementedError

    def train(self):
        raise NotImplementedError

    def predict(self, precedent_vector):
        """

        Predicts an outcome given a vector. Because the model is a regressive one,
        we replace all 0's with the average value of all the precedents.

        :param precedent_vector: numpy.array([1, 2, 5, 0, 223, 0, 0...])
        :return: [[int]]
        """
        data = self.mean_vector.copy()
        for i in range(len(precedent_vector)):
            if precedent_vector[i] > 0:
                data[i] = precedent_vector[i]
        return self.model.predict([data])

    def save(self):
        """
            Saves the scaler and regressor. Does not use joblib
            for the regressor as it is not supported
        """
        regressor_name = self.regressor_name
        file_path = os.path.join(Path.binary_directory, '{}_regressor.bin'.format(regressor_name))
        Log.write("saving" + '{}_regressor.bin'.format(regressor_name) + " to: " + file_path)
        Log.write('{}_regressor.bin'.format(regressor_name) + " saved to: " + file_path)
        self.model.steps[1][1].model.save(file_path)
        Save().save_binary('{}_scaler.bin'.format(regressor_name), self.model.steps[0][1])

    def load(self):
        """
            Loads the regressors different components
        """
        regressor_name = self.regressor_name
        Log.write("Loading " + '{}_regressor.bin'.format(regressor_name))
        file_path = os.path.join(Path.binary_directory, '{}_regressor.bin'.format(regressor_name))
        Log.write('{}_regressor.bin'.format(regressor_name) + " is successfully loaded")
        regressor = load_model(file_path)
        scaler = Load.load_binary('{}_scaler.bin'.format(regressor_name))
        self.model = AbstractRegressor._create_pipeline(scaler, regressor)
        self.mean_vector = Load.load_binary('regressor_means.bin')[self.regressor_name]

    @staticmethod
    def _create_pipeline(scaler, regressor):
        """
            Creates the pipeline of scaler + regressor
            and returns it.
        """
        estimators = []
        estimators.append(('standardize', scaler))
        estimators.append(('mlp', regressor))
        return Pipeline(estimators)

    def test(self):
        """
            Tests the regressor using the dataset and writes
            the mean and MSE of the deviation
        """
        seed = 7
        np.random.seed(seed)
        X = np.array([precedent['facts_vector'] for precedent in self.dataset])
        Y = np.array([precedent['outcomes_vector'][self.outcome_index]
                      for precedent in self.dataset])
        kfold = KFold(n_splits=10, random_state=seed)
        results = cross_val_score(self.model, X, Y, cv=kfold)
        Log.write("Mean: %.2f (%.2f) MSE" %
                  (results.mean(), results.std()))
