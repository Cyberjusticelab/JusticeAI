import numpy
from sys import stdout
import matplotlib.pyplot as plt
from ml_models.models import Load


class File:
    Epsilon = 'epsilon.txt'
    ClusterSize = 'cluster_size.txt'


def epsilon_histogram(data_matrix):
    """
    Creates a histogram of epsilon values
    :param data_matrix: numpy matrix
    :return: dictionary. Key --> epsilon values values --> density
    """
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
    return epsilon_hist


def cluster_size_histogram(data_matrix, epsilon):
    """
    Compute cluster size of histogrtam based on epsilon value
    :param data_matrix: numpy matrix of vectors
    :param epsilon: Epsilon value to compute with. Float
    :return:
    """
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
    return cluster_size_hist


if __name__ == '__main__':
    model = Load.load_decisions_from_bin()
    matrix = model[0]
    numpy.random.shuffle(matrix)
    hist = cluster_size_histogram(matrix[:3000], 0.2)
    X = list(hist.keys())
    Y = list(hist.values())
    plt.bar(X, Y)
    for i in range(len(X)):
        print(X[i], Y[i])
    plt.show()
