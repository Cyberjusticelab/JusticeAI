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

    Clustering algorithm using hdbscan

    output_directory <string>: output directory of clusters
    tpl <array, array, array>: vetors, transformed sentences, original sentence
    nb_of_files <int>: number of files to train on
    config <int, int>: configuration for TSNE manifold
    '''

    def train(self, output_directory, tpl, nb_of_files, config):
        data_matrix = tpl[0]
        sent = tpl[1]
        original_sent = tpl[2]
        data_matrix = self.manifold(data_matrix, config[0], config[1])
        print("Clustering")
        hdb = HDBSCAN(min_cluster_size=2).fit(data_matrix)
        hdb_labels = hdb.labels_
        n_clusters_hdb_ = len(set(hdb_labels)) - (1 if -1 in hdb_labels else 0)
        hdb_unique_labels = set(hdb_labels)
        self.__write_clusters(hdb_unique_labels, hdb_labels, output_directory, sent, original_sent)
        self.__write_metrics(output_directory, n_clusters_hdb_, nb_of_files, config)

    '''
    ------------------------------------------------------
    MANIFOLD
    ------------------------------------------------------
    Preprocessing for hdbscan
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

    def __write_clusters(self, unique_labels, labels, output_directory, sent, original_sent):
        for label in unique_labels:
            file = open(output_directory + str(label) + '.txt', 'w')

            for word in sent[labels == label]:
                file.writelines("[*] " + word)
                file.writelines('\n')

            file.writelines("-------------------------------\n")

            for word in original_sent[labels == label]:
                file.writelines("[*] " + word)
                file.writelines('\n')

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
    parser = Precedence_Parser()
    number_of_files = 100
    config = (200, 25)
    cluster_dir = r'cluster_dir/'
    clusterer = HdbscanTrain()

    start = time.time()

    tpl = parser.parse_topics(Global.Precedence_Directory, number_of_files)
    clusterer.train(cluster_dir, tpl, number_of_files, config)

    elapsed = time.time()
    print('Elapsed:')
    print(elapsed - start)
