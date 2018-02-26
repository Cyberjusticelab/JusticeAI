import numpy as np
from util.log import Log
from model_training.regression.single_output_regression.abstract_regressor import AbstractRegressor
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense

"""
    This regressor is used to determine how much money a tenant is
    supposed to pay a landlord. An implicit assumption of this regressor
    is that the tenant IS SUPPOSED TO PAY the landlord (i.e. non-zero value)
"""


class TenantPaysLandlord(AbstractRegressor):

    def __init__(self, dataset=None, outcome_index = 0):
        AbstractRegressor.__init__(self, 'tenant_pays_landlord', dataset, outcome_index)

    def train(self):
        """
            Trains the pipeline. After training the dataset is removed
            from the object to save space.
        """
        Log.write("Size of dataset: %d" % (len(self.dataset)))
        X = np.array([precedent['facts_vector'] for precedent in self.dataset])
        Y = np.array([precedent['outcomes_vector'][self.outcome_index]
                      for precedent in self.dataset])
        self.input_dimensions = len(X[0])
        regressor = KerasRegressor(
            build_fn=self._nn_architecture, epochs=100, batch_size=128, verbose=0)
        scaler = StandardScaler()
        self.model = AbstractRegressor._create_pipeline(scaler, regressor)
        self.model.fit(X, Y)
        self.test()
        self.dataset = None

    def _nn_architecture(self):
        """
                    Defines Regressor architecture. To be used internally
                """
        model = Sequential()
        model.add(Dense(13, input_dim=self.input_dimensions,
                        kernel_initializer='normal', activation='relu'))
        model.add(Dense(6, kernel_initializer='normal', activation='relu'))
        model.add(Dense(6, kernel_initializer='normal', activation='relu'))
        model.add(Dense(1, kernel_initializer='normal'))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model
