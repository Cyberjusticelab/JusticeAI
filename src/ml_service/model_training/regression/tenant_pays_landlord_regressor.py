from util.file import Load, Save
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
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
            self.dataset = [precedent for precedent in dataset.values() if precedent[
                'outcomes_vector'][10] > 1]
        else:
            self.load()

    def __adv_model():
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
        self.model.steps[1][1].model.save('tenant_pays_landlord_regressor.bin')
        Save().save_binary('tenant_pays_landlord_scaler.bin', self.model.steps[0][1])

    def load(self):
        """
            Loads the regressors different components
        """
        regressor = load_model('tenant_pays_landlord_regressor.bin')
        scaler = Load.load_binary('tenant_pays_landlord_scaler.bin')
        self.model = TenantPaysLandlordRegressor.__create_architecture(scaler, regressor)

    def train(self):
        Log.write("Size of dataset: %d" % (len(self.dataset)))
        X = np.array([precedent['facts_vector'] for precedent in self.dataset])
        Y = np.array([precedent['outcomes_vector'][10]
                      for precedent in self.dataset])
        regressor = KerasRegressor(
            build_fn=TenantPaysLandlordRegressor.__adv_model, epochs=100, batch_size=128, verbose=0)
        scaler = StandardScaler()
        self.model = TenantPaysLandlordRegressor.__create_architecture(scaler, regressor)
        self.model.fit(X, Y)
        self.dataset = None
        self.save()

    def __create_architecture(scaler, regressor):
        estimators = []
        estimators.append(('standardize', StandardScaler()))
        estimators.append(('mlp', regressor))
        return Pipeline(estimators)

    def test(self):
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
        return self.model.predict([precedent])

if __name__ == '__main__':
    precedents = Load.load_binary('precedent_vectors.bin')
    regressor = TenantPaysLandlordRegressor(precedents)
    regressor.train()
    precedents = [precedent for precedent in precedents.values() if precedent['outcomes_vector'][10] > 1]
    print("Test prediction with original regressor: %d" % (regressor.predict(precedents[0]['facts_vector'])))

    regressor = TenantPaysLandlordRegressor()
    print("Test prediction with loaded regressor: %d" % (regressor.predict(precedents[0]['facts_vector'])))
