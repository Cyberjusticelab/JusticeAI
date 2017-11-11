from src.ml_service.ml_models.models import load_facts_from_bin
from sklearn import decomposition
import matplotlib.pyplot as plt
import numpy
import math
import joblib
import os
from src.ml_service.reporting.logger import Log

def optimal_feature_size(matrix, evaluate_percent, plot=False):
    numpy.random.shuffle(matrix)
    pca = decomposition.PCA()
    percent = math.floor((len(matrix)) * evaluate_percent)
    pca.fit_transform(matrix[:percent])
    scores = pca.explained_variance_ratio_.cumsum()
    index = 0
    for variance in scores:
        if variance >= 0.95:
            break
        index += 1
    if plot:
        plt.hist(scores, bins=100)
        plt.show()
    return index

def decompose(matrix, size):
    pca = decomposition.PCA(n_components=size)
    result = pca.fit_transform(matrix)
    return result

def save_model(model):
    __script_dir = os.path.abspath(__file__ + "/../../../../")
    __rel_path = r'ml_models/updated_processed_facts'
    output_directory = os.path.join(__script_dir, __rel_path)
    joblib.dump(model, output_directory)

def execute():
    print("Matrix decomposition")
    Log.initialize(header='Matrix Decomposition', verbose=True)
    Log.report_start()
    model = load_facts_from_bin()
    matrix = model[0]
    sentence = model[1]
    processed_sentence = model[2]
    files = model[3]
    model = None
    Log.write("Computing optimal dimension reduction")
    size = optimal_feature_size(matrix, 1)
    Log.write('Optimal size: ' + str(size))
    Log.write("Decomposing matrix")
    new_matrix = decompose(matrix, size)
    Log.write('Saving Model')
    model = (new_matrix, sentence, processed_sentence, files)
    save_model(model)
    Log.report_end()


if __name__ == '__main__':
    execute()
