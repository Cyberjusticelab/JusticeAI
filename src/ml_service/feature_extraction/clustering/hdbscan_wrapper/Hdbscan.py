import os
import matplotlib.pyplot as plt
from hdbscan import HDBSCAN
from sklearn.manifold import TSNE
from src.ml_service.global_variables.global_variable import InformationType


class HdbscanTrain:
    def __init__(self):
        __script_dir = os.path.abspath(__file__ + "/../")
        __rel_path = r'cluster_dir/'
        self.output_directory = os.path.join(__script_dir, __rel_path)
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def train(self, data_tuple):
        """
        clustering algorithm using hdbscan_wrapper

        @:param data_tuple <array, array, array>: vectors, transformed sentences, original sentence
        """
        data_matrix = data_tuple[0]  # sentence vectors
        original_sent = data_tuple[1]  # original sentence
        print("clustering")
        hdb = HDBSCAN(min_cluster_size=30).fit(data_matrix)
        hdb_labels = hdb.labels_
        n_clusters_hdb_ = len(set(hdb_labels)) - (1 if -1 in hdb_labels else 0)
        hdb_unique_labels = set(hdb_labels)
        self.__write_clusters(hdb_unique_labels, hdb_labels, data_tuple)
        return hdb

    def manifold(self, data_matrix, learning_rate, perplexity):
        """
        preprocessing for hdbscan_wrapper
        Reduces dimension of vectors to yield much better results
        Reduces noise and groups up more similar terms

        data_matrix <numpy array>: vectors
        learning_rate <int>
        perplexity <int>
        """
        print("Standardizing matrix")
        print("Very long. please be patient. 10min for 2000 clusters")
        tsne = TSNE(n_components=2,
                    learning_rate=learning_rate,
                    perplexity=perplexity)
        return tsne.fit_transform(data_matrix)

    def __write_clusters(self, unique_labels, labels, data_tuple):
        """
        Writes 1 text file per cluster
        Every text file has the topics in the forms of:
        1- The sentence which was used to create a vector
        2- The original sentence from the text

        @:param unique_labels <int>: index of vector
        @:param labels <int>: index of vector
        @:param data_tuple <array, array, array>: vectors, transformed sentences, original sentence
        """
        for label in unique_labels:
            file = open(self.output_directory + str(label) + '.txt', 'w')
            for i, sent in enumerate(data_tuple[InformationType.FACTS.value][labels == label]):
                file.writelines(sent + '\n')
            file.writelines("-------------------------\n")
            for i, process_sent in enumerate(data_tuple[InformationType.PROCESSED_FACTS.value][labels == label]):
                file.writelines(process_sent + '\n')
            file.writelines("-------------------------\n")
            for i, filename in enumerate(data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][labels == label]):
                file.writelines(filename + '\n')
            file.close()

    def __write_metrics(self, output_directory, n_clusters_hdb_, nb_of_files, config):
        """
        Write metrics to text file and displays output

        @:param output_directory <string> : directory output
        @:param n_clusters_hdb_ <int> : number of created clusters
        @:param nb_of_files <int> : number of files used for training
        """
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
        """
        Plots the clusters

        @:param matrix <numpy array>: word vectors
        @:param sent <numpy array>: sentences in english
        """
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
