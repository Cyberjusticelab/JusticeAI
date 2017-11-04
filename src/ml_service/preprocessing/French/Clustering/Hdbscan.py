from hdbscan import HDBSCAN
from src.ml_service.preprocessing.French.DecisionParse import Precedence_Parser
from src.ml_service.preprocessing.French.GlobalVariable import Global
from src.ml_service.preprocessing.French.Vectorize import FrenchVectors
import os
import numpy as np


class hdbscan_train:
    def __init__(self, parser):
        self.parser = parser

    def train(self, file_directory,output_directory, file_num=None):
        data_matrix, sent = self.__create_matrix(file_directory, file_num)
        hdb = HDBSCAN(min_cluster_size=2).fit(data_matrix)
        hdb_labels = hdb.labels_
        n_clusters_hdb_ = len(set(hdb_labels)) - (1 if -1 in hdb_labels else 0)
        hdb_unique_labels = set(hdb_labels)

        for label in hdb_unique_labels:
            file = open(output_directory + str(label) + '.txt', 'w')
            for word in sent[hdb_labels == label]:
                file.writelines(word)
                file.writelines('\n')
            file.close()

        self.__write_metrics(output_directory, n_clusters_hdb_, file_num)

    def __create_matrix(self, file_directory, file_num):
        j = 0
        data = []
        sent = []
        for i in os.listdir(file_directory):
            if (file_num is not None) and (j >= file_num):
                 break
            j += 1
            model = self.parser.parse(i)
            for i in range(len(model.core_topic)):
                if model.topics[i] in sent:
                    continue
                vec = FrenchVectors.vectorize_sent(model.core_topic[i])
                data.append(vec)
                sent.append(model.topics[i])
        return np.array(data), np.array(sent)

    def __write_metrics(self, output_directory, n_clusters_hdb_, file_num):
        num_lines = sum(1 for line in open(output_directory + '-1.txt'))

        file = open('first_pass_metrics.txt', 'a')
        file.write('Number_of_clusters: ' + str(n_clusters_hdb_) + '\t')
        file.write('Number_of_files used: ' + str(file_num) + '\t')
        file.write('Noise: ' + str(num_lines) + '\n')
        file.close()

        print('Number_of_clusters: ' + str(n_clusters_hdb_))
        print('Number_of_files_used: ' + str(file_num))
        print('Noise: ' + str(num_lines))


if __name__ == '__main__':
    parser = Precedence_Parser()
    clusterer = hdbscan_train(parser)
    first_pass_dir = r'first_pass/'
    clusterer.train(Global.Precedence_Directory, first_pass_dir, 10)