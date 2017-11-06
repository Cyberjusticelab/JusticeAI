import numpy as np
from hdbscan import HDBSCAN
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import time
from src.ml_service.GlobalVariables.GlobalVariable import Global
from src.ml_service.feature_extraction.Preprocessing.Sam_Parser.PrecedenceParse import Precedence_Parser


class HdbscanTrain:
    def __init__(self):
        pass

    '''
    ------------------------------------------------------
    Train
    ------------------------------------------------------
    
    Clustering algorithm using HDBSCAN
    
    file_directory <string>: precedence file directory
    output_directory <string>: output directory of clusters
    nb_of_files <int>: number of files to train on
    plot <bool>: plot the graph of the clusters
    '''

    def train(self, output_directory, data_matrix, sent, original_sent, nb_of_files, config, plot=False):
        print("Standardizing matrix")
        tsne = TSNE(n_components=2,
                    learning_rate=config[0],
                    perplexity=config[1])
        data_matrix = tsne.fit_transform(data_matrix)
        print("Clustering")
        hdb = HDBSCAN(min_cluster_size=2).fit(data_matrix)
        hdb_labels = hdb.labels_
        n_clusters_hdb_ = len(set(hdb_labels)) - (1 if -1 in hdb_labels else 0)
        hdb_unique_labels = set(hdb_labels)

        hdb_colors = plt.cm.Spectral(np.linspace(0, 1, len(hdb_unique_labels)))
        fig = plt.figure(figsize=plt.figaspect(0.5))
        hdb_axis = fig.add_subplot('121')  # value 121 taken from demo found on github

        for label, col in zip(hdb_unique_labels, hdb_colors):
            file = open(output_directory + str(label) + '.txt', 'w')

            for word in sent[hdb_labels == label]:
                file.writelines("[*] " + word)
                file.writelines('\n')

            file.writelines("-------------------------------\n")

            for word in original_sent[hdb_labels == label]:
                file.writelines("[*] " + word)
                file.writelines('\n')

            file.close()
            if label == -1:
                # Black used for noise.
                col = 'k'
            hdb_axis.plot(data_matrix[hdb_labels == label, 0],
                          data_matrix[hdb_labels == label, 1],
                          'o',
                          markerfacecolor=col,
                          markeredgecolor='k',
                          markersize=6)

        self.__write_metrics(output_directory, n_clusters_hdb_, nb_of_files, config)
        if plot:
            plt.show()

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
    parser = Precedence_Parser()
    number_of_files = [8000]
    config = (200, 22)
    start = time.time()
    for i in number_of_files:
        data_matrix, sent, original_sent = parser.parse_training_data(Global.Precedence_Directory, i)
        clusterer = HdbscanTrain()
        cluster_dir = r'cluster_dir/'
        #clusterer.plot(data_matrix, sent)
        clusterer.train(cluster_dir, data_matrix, sent, original_sent, i, config)
    elapsed = time.time()
    print('Elapsed:')
    print(elapsed - start)
