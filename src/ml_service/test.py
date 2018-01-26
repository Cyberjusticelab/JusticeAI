import joblib
# from model_training.regression.multi_class_svr import MultiClassSVR
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np

prec = joblib.load('/home/arekmano/workspace/JusticeAI/src/ml_service/data/binary/precedent_vectors.bin')
aa = [prece for prece in prec.values() if prece['demands_vector'][2] > 0 or prece['demands_vector'][11] > 0]

print("Size of dataset: %d" % (len(aa)))
# load dataset
# split into input (X) and output (Y) variables
X = np.array([a['facts_vector'] for a in aa])
Y = np.array([a['outcomes_vector'][10] for a in aa])

# define base model
def vadv_model():
    # create model
    model = Sequential()
    model.add(Dense(13, input_dim=51, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_absolute_percentage_error', optimizer='adam')
    return model



# define base model
def adv_model():
    # create model
    model = Sequential()
    model.add(Dense(13, input_dim=51, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_absolute_percentage_error', optimizer='adam')
    return model

def intermed_model():
    # create model
    model = Sequential()
    model.add(Dense(13, input_dim=51, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_absolute_percentage_error', optimizer='adam')
    return model

def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(13, input_dim=51, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

# fix random seed for reproducibility
seed = 7

# evaluate model with standardized dataset
np.random.seed(seed)

for x in range(0, 5):
    epochs = (x + 1) * 50
    regressor = KerasRegressor(build_fn=baseline_model, epochs=epochs, batch_size=128, verbose=0)
    estimators = []
    estimators.append(('standardize', StandardScaler()))
    estimators.append(('mlp', regressor))
    pipeline = Pipeline(estimators)
    kfold = KFold(n_splits=10, random_state=seed)
    results = cross_val_score(pipeline, X, Y, cv=kfold)
    print("Standardized: %.2f (%.2f) MSE, model: baseline_model, epochs: %d" % (results.mean(), results.std(), epochs))

    regressor = KerasRegressor(build_fn=intermed_model, epochs=epochs, batch_size=128, verbose=0)
    estimators = []
    estimators.append(('standardize', StandardScaler()))
    estimators.append(('mlp', regressor))
    pipeline = Pipeline(estimators)
    kfold = KFold(n_splits=10, random_state=seed)
    results = cross_val_score(pipeline, X, Y, cv=kfold)
    print("Standardized: %.2f (%.2f) MSE, model: intermed_model, epochs: %d" % (results.mean(), results.std(), epochs))

    regressor = KerasRegressor(build_fn=adv_model, epochs=epochs, batch_size=128, verbose=0)
    estimators = []
    estimators.append(('standardize', StandardScaler()))
    estimators.append(('mlp', regressor))
    pipeline = Pipeline(estimators)
    kfold = KFold(n_splits=10, random_state=seed)
    results = cross_val_score(pipeline, X, Y, cv=kfold)
    print("Standardized: %.2f (%.2f) MSE, model: adv_model, epochs: %d" % (results.mean(), results.std(), epochs))

    regressor = KerasRegressor(build_fn=vadv_model, epochs=epochs, batch_size=128, verbose=0)
    estimators = []
    estimators.append(('standardize', StandardScaler()))
    estimators.append(('mlp', regressor))
    pipeline = Pipeline(estimators)
    kfold = KFold(n_splits=10, random_state=seed)
    results = cross_val_score(pipeline, X, Y, cv=kfold)
    print("Standardized: %.2f (%.2f) MSE, model: vadv_model, epochs: %d" % (results.mean(), results.std(), epochs))

# for x in range(0, 10):
#     epochs = (x + 1) * 100
#     regressor = KerasRegressor(build_fn=vadv_model, epochs=epochs, batch_size=128, verbose=0)
#     estimators = []
#     estimators.append(('standardize', StandardScaler()))
#     estimators.append(('mlp', regressor))
#     pipeline = Pipeline(estimators)
#     kfold = KFold(n_splits=10, random_state=seed)
#     results = cross_val_score(pipeline, X, Y, cv=kfold)
#     print("Standardized: %.2f (%.2f) MSE, epochs: %d" % (results.mean(), results.std(), epochs))

