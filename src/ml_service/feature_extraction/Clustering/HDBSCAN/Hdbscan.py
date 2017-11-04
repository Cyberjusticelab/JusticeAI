import matplotlib.pyplot as plt
import numpy as np
from hdbscan import HDBSCAN

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
    def train(self, output_directory, data_matrix, sent, nb_of_files, plot=False):
        hdb = HDBSCAN(min_cluster_size=2).fit(data_matrix)

        hdb_labels = hdb.labels_
        n_clusters_hdb_ = len(set(hdb_labels)) - (1 if -1 in hdb_labels else 0)
        hdb_unique_labels = set(hdb_labels)

        hdb_colors = plt.cm.Spectral(np.linspace(0, 1, len(hdb_unique_labels)))
        fig = plt.figure(figsize=plt.figaspect(0.5))
        hdb_axis = fig.add_subplot('121') # value 121 taken from demo found on github

        for label, col in zip(hdb_unique_labels, hdb_colors):
            file = open(output_directory + str(label) + '.txt', 'w')
            for word in sent[hdb_labels == label]:
                file.writelines(word)
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

        self.__write_metrics(output_directory, n_clusters_hdb_, nb_of_files)
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
    def __write_metrics(self, output_directory, n_clusters_hdb_, nb_of_files):
        num_lines = sum(1 for line in open(output_directory + '-1.txt'))

        file = open('metrics.txt', 'a')
        file.write('Number_of_clusters: ' + str(n_clusters_hdb_) + '\t')
        file.write('Number_of_files used: ' + str(nb_of_files) + '\t')
        file.write('Noise: ' + str(num_lines) + '\n')
        file.close()

        print('Number_of_clusters: ' + str(n_clusters_hdb_))
        print('Number_of_files_used: ' + str(nb_of_files))
        print('Noise: ' + str(num_lines))


if __name__ == '__main__':
    parser = Precedence_Parser()
    number_of_files = [10, 100, 500, 1000, 2000, 4000, 8000, 16000, 32000]
    for i in number_of_files:
        data_matrix, sent = parser.parse_training_data(Global.Precedence_Directory, i)
        clusterer = HdbscanTrain()
        cluster_dir = r'cluster_dir/'
        clusterer.train(cluster_dir, data_matrix, sent, i)