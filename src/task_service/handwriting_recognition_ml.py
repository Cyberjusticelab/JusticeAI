import tensorflow as tf

sess = tf.InteractiveSession()

import keras
import numpy as np

from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D
from keras.layers import Flatten, Lambda, BatchNormalization
from keras.models import Sequential
from keras.optimizers import Adam as Adam
from keras.layers.advanced_activations import LeakyReLU

# used to save and load training histories
import pickle
from collections import defaultdict

import resource
import sys

# we would reach recursion limit when saving training history otherwise
resource.setrlimit(resource.RLIMIT_STACK, (2 ** 29, -1))
sys.setrecursionlimit(2 ** 29 - 1)
from scipy import io as spio

emnist = spio.loadmat("datasets/matlab/emnist-digits.mat")
# load training dataset
x_train = emnist["dataset"][0][0][0][0][0][0]
x_train = x_train.astype(np.float32)

# load training labels
y_train = emnist["dataset"][0][0][0][0][0][1]
# load test dataset
x_test = emnist["dataset"][0][0][1][0][0][0]
x_test = x_test.astype(np.float32)

# load test labels
y_test = emnist["dataset"][0][0][1][0][0][1]
# store labels for visualization
train_labels = y_train
test_labels = y_test

# normalize
x_train /= 255
x_test /= 255
# reshape using matlab order
x_train = x_train.reshape(x_train.shape[0], 1, 28, 28, order="A")
x_test = x_test.reshape(x_test.shape[0], 1, 28, 28, order="A")
# labels should be onehot encoded
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

test_labels = test_labels.reshape(40000)

mean_px = x_train.mean().astype(np.float32)
std_px = x_train.std().astype(np.float32)


def norm_input(x): return (x - mean_px) / std_px


# Batchnorm + dropout + data augmentation
def create_model():
    model = Sequential([
        Lambda(norm_input, input_shape=(1, 28, 28), output_shape=(1, 28, 28)),
        Conv2D(32, (3, 3), data_format='channels_first'),
        LeakyReLU(),
        BatchNormalization(axis=1),
        Conv2D(32, (3, 3), data_format='channels_first'),
        LeakyReLU(),
        MaxPooling2D(),
        BatchNormalization(axis=1),
        Conv2D(64, (3, 3), data_format='channels_first'),
        LeakyReLU(),
        BatchNormalization(axis=1),
        Conv2D(64, (3, 3), data_format='channels_first'),
        LeakyReLU(),
        MaxPooling2D(),
        Flatten(),
        BatchNormalization(),
        Dense(512),
        LeakyReLU(),
        BatchNormalization(),
        Dropout(0.2),
        Dense(10, activation='softmax')
    ])
    model.compile(Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
    return model


batch_size = 512
from keras.preprocessing.image import ImageDataGenerator

gen = ImageDataGenerator(rotation_range=12, width_shift_range=0.1, shear_range=0.3,
                         height_shift_range=0.1, zoom_range=0.1, data_format='channels_first')
batches = gen.flow(x_train, y_train, batch_size=batch_size)
test_batches = gen.flow(x_test, y_test, batch_size=batch_size)
steps_per_epoch = int(np.ceil(batches.n / batch_size))
validation_steps = int(np.ceil(test_batches.n / batch_size))

models = []
models.append(create_model())

eval_batch_size = 512
num_iterations = 1
num_epochs = 1
weights_epoch = 0

for iteration in range(num_iterations):
    cur_epoch = (iteration + 1) * num_epochs + weights_epoch
    print("iteration {}, cur_epoch {}".format(iteration + 1, cur_epoch))

    # train models for specified number of epochs
    for i, m in enumerate(models):
        m.optimizer.lr = 0.000001
        h = m.fit_generator(batches, steps_per_epoch=steps_per_epoch, epochs=num_epochs, verbose=0,
                            validation_data=test_batches, validation_steps=validation_steps)

        # save model weights
        m.save_weights("dropout_0.2/weights/{:03d}epochs_weights_model_{}.pkl".format(cur_epoch, i))

        # save corresponding training history (broken right now)
        # TypeError: can't pickle _thread.lock objects
        # with open("dropout_0.2/history/{:03d}epochs_history_model_{}.pkl".format(cur_epoch, i),"wb") as f:
        #    pickle.dump(h, f)

    # evaluate test error rate for ensemble
    all_preds = np.stack([m.predict(x_test, batch_size=eval_batch_size) for m in models])
    avg_preds = all_preds.mean(axis=0)
    test_error_ensemble = (1 - keras.metrics.categorical_accuracy(y_test, avg_preds).eval().mean()) * 100

    # write test error rate for ensemble and every single model to text file
    with open("dropout_0.2/history/test_errors_epoch_{:03d}.txt".format(cur_epoch), "w") as text_file:
        text_file.write("epoch: {} test error on ensemble: {}\n".format(cur_epoch, test_error_ensemble))

        for m in models:
            pred = np.array(m.predict(x_test, batch_size=eval_batch_size))
            test_err = (1 - keras.metrics.categorical_accuracy(y_test, pred).eval().mean()) * 100
            text_file.write("{}\n".format(test_err))
