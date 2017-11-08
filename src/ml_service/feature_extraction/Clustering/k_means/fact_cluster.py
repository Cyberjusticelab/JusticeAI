import re
import nltk
import os
from nltk.stem.snowball import SnowballStemmer
from sklearn.cluster import KMeans


class KMeansWrapper:
    def __init__(self, data_tuple):
        """
        :param precedent_directory: directory path precedents
        :param total_file_to_process: amount of files to process
        :param cluster_size: amount of cluster to look for
        """
        __script_dir = os.path.abspath(__file__ + "/../")
        __rel_path = r'cluster_dir/'
        self.output_directory = os.path.join(__script_dir, __rel_path)
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        self.claim_text = data_tuple[1]  # original sentence
        self.data_matrix = data_tuple[0]  # sentence vector
        self.cluster_size = 100
        self.km = self.cluster()
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
        for label in unique_labels:
            file = open(self.output_directory + str(label) + '.txt', 'w')
            for i, sent in enumerate(self.data_tuple[1][clusters == label]):
                file.writelines(sent + '\n')  # original sentence

            file.writelines("-------------------------\n")
            for i, process_sent in enumerate(self.data_tuple[3][clusters == label]):
                file.writelines(process_sent + '\n')  # processed sentence

            file.writelines("-------------------------\n")
            for i, filename in enumerate(self.data_tuple[2][clusters == label]):
                file.writelines(filename + '\n')  # filename

            file.close()
