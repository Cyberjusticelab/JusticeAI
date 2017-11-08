from hdbscan import HDBSCAN
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import time
from src.ml_service.GlobalVariables.GlobalVariable import Global
from src.ml_service.feature_extraction.Preprocessing.Sam_Parser.PrecedenceParse import Precedence_Parser
import os


class HdbscanTrain:
    def __init__(self):
        __script_dir = os.path.abspath(__file__ + "/../")
        __rel_path = r'cluster_dir/'
        self.output_directory = os.path.join(__script_dir, __rel_path)
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    '''
    ------------------------------------------------------
    Train
    ------------------------------------------------------

    Clustering algorithm using hdbscan_wrapper

    output_directory <string>: output directory of clusters
    tpl <array, array, array>: vetors, transformed sentences, original sentence
    nb_of_files <int>: number of files to train on
    config <int, int>: configuration for TSNE manifold
    '''

    def train(self, data_tuple):
        data_matrix = data_tuple[0]  # sentence vectors
        original_sent = data_tuple[1]  # original sentence
        data_matrix = self.manifold(data_matrix, 200, 24)
        print("Clustering")
        hdb = HDBSCAN(min_cluster_size=2).fit(data_matrix)
        hdb_labels = hdb.labels_
        n_clusters_hdb_ = len(set(hdb_labels)) - (1 if -1 in hdb_labels else 0)
        hdb_unique_labels = set(hdb_labels)
        self.__write_clusters(hdb_unique_labels, hdb_labels, data_tuple)

    '''
    ------------------------------------------------------
    MANIFOLD
    ------------------------------------------------------
    Preprocessing for hdbscan_wrapper
    Reduces dimension of vectors to yield much better results
    Reduces noise and groups up more similar terms

    data_matrix <numpy array>: vectors
    learning_rate <int>
    perplexity <int>
    '''

    def manifold(self, data_matrix, learning_rate, perplexity):
        print("Standardizing matrix")
        tsne = TSNE(n_components=2,
                    learning_rate=learning_rate,
                    perplexity=perplexity)
        return tsne.fit_transform(data_matrix)

    '''
    ------------------------------------------------------
    WRITE CLUSTERS
    ------------------------------------------------------
    Writes 1 text file per cluster
    Every text file has the topics in the forms of:
    1- The sentence which was used to create a vector
    2- The original sentence from the text

    hdb_unique_labels <int>: index of vector
    hdb_labels <int>: index of vector
    output_directory <string>: directory
    sent <numpy array>: sentences for vectors
    original_sent <numpy array>: original sentences
    '''

    def __write_clusters(self, unique_labels, labels, data_tuple):
        for label in unique_labels:
            file = open(self.output_directory + str(label) + '.txt', 'w')
            for i, sent in enumerate(data_tuple[1][labels == label]):
                file.writelines(sent + '\n')

            for i, process_sent in enumerate(data_tuple[3][labels == label]):
                file.writelines(process_sent + '\n')

            for i, filename in enumerate(data_tuple[2][labels == label]):
                file.writelines(filename + '\n')
            file.close()

    '''
    ------------------------------------------------------
    Write Metrics
    ------------------------------------------------------
    Write metrics to text file and displays output

    output_directory <string> : directory output
    n_clusters_hdb_ <int> : number of created clusters
    nb_of_files <int> : number of files used for training
    '''

    def __write_metrics(self, output_directory, n_clusters_hdb_, nb_of_files, config):
        num_lines = sum(1 for line in open(output_directory + '-1.txt'))

        file = open('metrics.txt', 'a')
        file.write('Number_of_clusters: ' + str(n_clusters_hdb_) + '\t')
        file.write('Number_of_files used: ' + str(nb_of_files) + '\t')
        file.write('Noise: ' + str(num_lines) + '\t')
        file.write('Learning rate: ' + str(config[0]) + '\t')
        file.write('Perplexity: ' + str(config[1]) + '\n')
        file.close()

        print('Number_of_clusters: ' + str(n_clusters_hdb_))
        print('Number_of_files_used: ' + str(nb_of_files))
        print('Noise: ' + str(num_lines))

    '''
    ------------------------------------------------------
    PLOT
    ------------------------------------------------------

    Plots the clusters

    matrix <numpy array>: word vectors
    sent <numpy array>: sentences in english
    '''

    def plot(self, matrix, sent):
        tsne = TSNE(n_components=2,
                    learning_rate=300,
                    perplexity=10)
        Y = tsne.fit_transform(matrix)
        plt.scatter(Y[:, 0], Y[:, 1])
        for label, x, y in zip(sent, Y[:, 0], Y[:, 1]):
            plt.annotate('', xy=(x, y), xytext=(0, 0), textcoords='offset points')
        plt.show()


if __name__ == '__main__':
    pass
