from util.file import Load, Save
from util.constant import Path
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import os
import numpy as np
from util.log import Log

"""
    This regressor is used to determine how much money a tenant is
    supposed to pay a landlord. An implicit assumption of this regressor
    is that the tenant IS SUPPOSED TO PAY the landlord (i.e. non-zero value)
"""
class TenantPaysLandlordRegressor:

    def __init__(self, dataset=None):
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
        if dataset is not None:
            self.dataset = [precedent for precedent in dataset if precedent[
                'outcomes_vector'][10] > 1]
        else:
            self.load()

    @staticmethod
    def __nn_architecture():
        """
            Defines Regressor architecture. To be used internally
        """
        model = Sequential()
        model.add(Dense(13, input_dim=51,
                        kernel_initializer='normal', activation='relu'))
        model.add(Dense(6, kernel_initializer='normal', activation='relu'))
        model.add(Dense(6, kernel_initializer='normal', activation='relu'))
        model.add(Dense(1, kernel_initializer='normal'))
        model.compile(loss='mean_absolute_percentage_error', optimizer='adam')
        return model

    def save(self):
        """
            Saves the scaler and regressor. Does not use joblib
            for the regressor as it is not supported
        """
        file_path = os.path.join(Path.binary_directory, 'tenant_pays_landlord_regressor.bin')
        Log.write("saving" + 'tenant_pays_landlord_regressor.bin' + " to: " + file_path)
        Log.write('tenant_pays_landlord_regressor.bin' + " saved to: " + file_path)
        self.model.steps[1][1].model.save(file_path)
        Save().save_binary('tenant_pays_landlord_scaler.bin', self.model.steps[0][1])

    def load(self):
        """
            Loads the regressors different components
        """
        Log.write("Loading " + 'tenant_pays_landlord_regressor.bin')
        file_path = os.path.join(Path.binary_directory, 'tenant_pays_landlord_regressor.bin')
        Log.write('tenant_pays_landlord_regressor.bin' + " is successfully loaded")
        regressor = load_model(file_path)
        scaler = Load.load_binary('tenant_pays_landlord_scaler.bin')
        self.model = TenantPaysLandlordRegressor.__create_pipeline(scaler, regressor)

    def train(self):
        """
            Trains the pipeline. After training the dataset is removed
            from the object to save space.
        """
        Log.write("Size of dataset: %d" % (len(self.dataset)))
        X = np.array([precedent['facts_vector'] for precedent in self.dataset])
        Y = np.array([precedent['outcomes_vector'][10]
                      for precedent in self.dataset])
        regressor = KerasRegressor(
            build_fn=TenantPaysLandlordRegressor.__nn_architecture, epochs=100, batch_size=128, verbose=0)
        scaler = StandardScaler()
        self.model = TenantPaysLandlordRegressor.__create_pipeline(scaler, regressor)
        self.model.fit(X, Y)
        self.test()

    @staticmethod
    def __create_pipeline(scaler, regressor):
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
        Y = np.array([precedent['outcomes_vector'][10]
                      for precedent in self.dataset])
        kfold = KFold(n_splits=10, random_state=seed)
        results = cross_val_score(self.model, X, Y, cv=kfold)
        Log.write("Mean: %.2f (%.2f) MSE" %
                  (results.mean(), results.std()))

    def predict(self, precedent):
        """
            Predicts the tenant_ordered_to_pay_landlord outcome
            and returns it
            param: precedent: fact vector in the form of np.array([1,0,1,0,2])
            returns: predicted integer value of tenant_ordered_to_pay_landlord
        """
        return self.model.predict([precedent])

