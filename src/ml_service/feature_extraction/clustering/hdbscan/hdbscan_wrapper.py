from hdbscan import HDBSCAN
from src.ml_service.global_variables.global_variable import InformationType
from src.ml_service.outputs.output import Save
from src.ml_service.outputs.output import Log


class HdbscanTrain:
    def __init__(self):
        pass

    def cluster(self, data_tuple, min_cluster_size, min_sample):
        """
        clustering algorithm using hdbscan
        @:param data_tuple (vectors, sentences, filenames)
        """
        Log.write('Starting HDBSCAN')
        Log.write('Min Cluster Size: ' + str(min_cluster_size))
        Log.write('Min Sample: ' + str(min_sample))
        hdb = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_sample).fit(data_tuple[0])
        s = Save(r'hdb_model/')
        s.binarize_model('hdbscan.bin', hdb)
        hdb_unique_labels = set(hdb.labels_)
        n_clusters_hdb_ = len(hdb_unique_labels) - (1 if -1 in hdb.labels_ else 0)
        self.__write_clusters(hdb_unique_labels, hdb.labels_, data_tuple)
        Log.write('Estimated clusters:' + str(n_clusters_hdb_))
        return hdb

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
        s = Save('hdb_cluster_dir')
        for label in unique_labels:
            text = []
            for i, sent in enumerate(data_tuple[InformationType.FACTS.value][labels == label]):
                text.append(sent)
            text.append("\n------------------------------------------\n")

            for i, filename in enumerate(data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][labels == label]):
                text.append(filename)
            s.save_text_file(str(label) + '.txt', text, 'w')

    def __log_metrics(self, output_directory, n_clusters_hdb_, nb_of_files, config):
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
