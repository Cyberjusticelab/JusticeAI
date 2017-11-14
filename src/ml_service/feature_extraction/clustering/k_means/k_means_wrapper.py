import re
import nltk
import os
from nltk.stem.snowball import SnowballStemmer
from sklearn.cluster import KMeans
from global_variables.global_variable import InformationType
from outputs.output import Save


class KMeansWrapper:
    def __init__(self, data_tuple):
        """
        :param precedent_directory: directory path precedents
        :param total_file_to_process: amount of files to process
        :param cluster_size: amount of cluster to look for
        """
        self.claim_text = data_tuple[1]  # original sentence
        self.data_matrix = data_tuple[0]  # sentence vector
        self.cluster_size = 100  # numbers of cluster desired
        self.km = self.cluster()
        s = Save(r'kmean_model/')
        s.binarize_model('kmeans.bin', self.km)
        self.data_tuple = data_tuple
        self.print_cluster()

    def tokenize_and_stem(self, text):
        stemmer = SnowballStemmer("french")
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems

    def tokenize_only(self, text):
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        return filtered_tokens

    def cluster(self):
        km = KMeans(n_clusters=self.cluster_size, init='k-means++')
        km.fit(self.data_matrix)
        return km

    def print_cluster(self):
        clusters = self.km.labels_
        unique_labels = set(clusters)
        s = Save(r'k_means')
        for label in unique_labels:
            text = []
            for i, sent in enumerate(self.data_tuple[InformationType.FACTS.value][clusters == label]):
                text.append(sent)
            text.append("\n------------------------------------------\n")

            for i, filename in enumerate(self.data_tuple[InformationType.PRECEDENTS_FILE_NAMES.value][labels == label]):
                text.append(filename)
            s.save_text_file(str(label) + '.txt', text, 'w')
