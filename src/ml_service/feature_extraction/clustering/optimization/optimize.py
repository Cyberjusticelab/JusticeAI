import numpy
import json
from sys import stdout
from src.ml_service.ml_models.models import Load
import matplotlib.pyplot as plt


class File:
    Epsilon = 'epsilon.txt'
    ClusterSize = 'cluster_size.txt'


def epsilon_histogram(data_matrix):
    epsilon_hist = {}
    for i in range(len(data_matrix)):
        percent = float(i / len(data_matrix)) * 100
        stdout.write("\rComputation: %f " % percent)
        stdout.flush()

        min_val = -1
        for j in range(len(data_matrix)):
            if i == j:
                continue
            dist = numpy.linalg.norm(data_matrix[i] - data_matrix[j])
            # decimal places
            dist = "%.1f" % dist
            if min_val == -1:
                min_val = dist
            elif dist < min_val:
                min_val = dist
        if min_val in epsilon_hist:
            epsilon_hist[min_val] += 1
        else:
            epsilon_hist[min_val] = 1
    save_histogram(epsilon_hist, File.Epsilon)
    return epsilon_hist


def cluster_size_histogram(data_matrix, epsilon):
    cluster_size_hist = {}
    for i in range(len(data_matrix)):
        percent = float(i / len(data_matrix)) * 100
        stdout.write("\rComputation: %f " % percent)
        stdout.flush()

        cluster_size = 0
        for j in range(len(data_matrix)):
            dist = numpy.linalg.norm(data_matrix[i] - data_matrix[j])
            if dist <= epsilon:
                cluster_size += 1
        if cluster_size in cluster_size_hist:
            cluster_size_hist[cluster_size] += 1
        else:
            cluster_size_hist[cluster_size] = 1
    save_histogram(cluster_size_hist, File.ClusterSize)
    return cluster_size_hist


def save_histogram(array, filename):
    with open(filename, 'w') as fp:
        json.dump(array, fp)


if __name__ == '__main__':
    model = Load.load_facts_from_bin()
    matrix = model[0]
    model = None
    numpy.random.shuffle(matrix)
    #hist = epsilon_histogram(matrix[:6000])
    hist = cluster_size_histogram(matrix[:3000], 1.0)
    X = list(hist.keys())
    Y = list(hist.values())
    plt.bar(X, Y)
    plt.show()
