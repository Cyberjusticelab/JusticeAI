from util.file import Load, Save
from util.constant import Path
from keras.models import load_model
from sklearn import metrics
from sklearn.pipeline import Pipeline
import os
import numpy as np
from util.log import Log
from model_training.classifier.multi_output.multi_class_svm import MultiClassSVM
from feature_extraction.post_processing.regex.regex_tagger import TagPrecedents


class AbstractRegressor:

    def __init__(self, regressor_name, dataset=None, outcome_index=0):
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
        self.regressor_name = regressor_name
        self.input_dimensions = None
        self.model = None
        self.mean_facts_vector = None
        self.outcome_index = None
        self.dataset = None
        try:
            facts = MultiClassSVM().get_ordered_weights()[regressor_name]['important_facts']
            facts += MultiClassSVM().get_ordered_weights()[regressor_name]['additional_facts']
            facts_index = TagPrecedents().get_intent_index()['facts_vector']
            self.important_facts_index = [x[0] for x in facts_index if x[1] in facts]
        except:
            pass
        if dataset is not None:
            self.__filter_dataset(dataset, outcome_index)
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
        precedent_vector = precedent_vector[self.important_facts_index]
        data = self.mean_facts_vector.copy()
        data = data[self.important_facts_index]
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
        Save().save_binary('model_metrics.bin', self.data_metrics())
        self.dataset = None

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
        self.mean_facts_vector = Load.load_binary('model_metrics.bin')['regressor'][regressor_name]['mean_facts_vector']

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
        Tests the regressor using the dataset and writes:
            1- coefficient r2
            2- explained variance
            3- mean absolute error
            4- mean squared error

        :return: None
        """
        X = np.array([precedent['facts_vector'][self.important_facts_index] for precedent in self.dataset])
        y_pred = self.model.predict(X)
        y_true = np.array([precedent['outcomes_vector'][self.outcome_index]
                           for precedent in self.dataset])
        r2 = metrics.r2_score(y_true, y_pred)
        variance = metrics.explained_variance_score(y_true, y_pred)
        mean_abs_error = metrics.mean_absolute_error(y_true, y_pred)
        mean_squared_error = metrics.mean_squared_error(y_true, y_pred)
        Log.write('R2: {0:.2f}'.format(r2))
        Log.write('Explained Variance: {0:.2f}'.format(variance))
        Log.write('Mean Absolute Error: {0:.2f}'.format(mean_abs_error))
        Log.write('Mean Squared Error: {0:.2f}'.format(mean_squared_error))

    def data_metrics(self):
        """
        1) Obtain the fact vectors
        2) Obtain the outcome vectors pertaining to the regressor in question
        3) Collect data metrics
            3.1) mean_fact_vector --> the average of every fact column
            3.2) standard deviation of outcomes
            3.3) variance of outcomes
            3.4) mean of outcomes
        4) persist data into a dictionary which will be binarized

        model_metrics -->
        {
            'data_set':{
                'size': 5000
            },
            'regressor':{
                'regressor name':{
                    'std': 4,
                    'mean': 5,
                    'variance': 42,
                    'mean_fact_vector': [3, 1, 5, 6, 2]
                }
            },
            'classifier':{
                'classifier name':{
                    'prediction_accuracy': 0.92,
                }
            }
        }
        :return: model_metrics
        """

        facts_vector = [x['facts_vector'] for x in self.dataset]
        outcomes_vector = [x['outcomes_vector'][self.outcome_index] for x in self.dataset]

        model_metrics = Load.load_binary('model_metrics.bin')
        if model_metrics is None:
            model_metrics = {
                'regressor': {
                    self.regressor_name: {

                    }
                }
            }
        elif 'regressor' not in model_metrics:
            model_metrics['regressor'] = {}

        self.mean_facts_vector = np.mean(facts_vector, axis=0)
        model_metrics['regressor'][self.regressor_name] = {
            'mean_facts_vector': self.mean_facts_vector,
            'std': np.std(outcomes_vector),
            'variance': np.var(outcomes_vector),
            'mean': np.mean(outcomes_vector)
        }

        return model_metrics

    def __filter_dataset(self, dataset, outcome_index):
        """
        The dataset is filtered to train the regressor:
            1- Based on facts which were determined to have considerable
               weight by the classifier.
            2- If the outcome is present in a decision (biased)
            3- If the outcome isn't an outlier

        Outlier detection:
            1- Find standard deviation of outcomes
            2- Find mean of outcomes
            3- if (abs(outcome - mean) < (2 * std)) then it is NOT an outlier

        :param dataset: [{
            name: 'AZ-XXXXXXX.txt',
            demands_vector: [...],
            facts_vector: [...],
            outcomes_vector: [...]
        },
        {
            ...
        }]
        :param outcome_index: integer
        :return: None
        """
        outcomes = [x['outcomes_vector'][outcome_index] for x in dataset if x[
            'outcomes_vector'][outcome_index] > 1]
        std = np.std(outcomes)
        mean = np.mean(outcomes)
        self.dataset = [precedent for precedent in dataset if (precedent[
                                                                   'outcomes_vector'][outcome_index] > 1) and
                        (abs(precedent['outcomes_vector'][outcome_index] - mean) < (2 * std))]
        self.outcome_index = outcome_index
