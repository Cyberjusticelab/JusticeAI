import re
import nltk
from nltk.stem.snowball import SnowballStemmer
from sklearn.cluster import KMeans


class KMeansWrapper:
    def __init__(self, data_tuple):
        """
        :param precedent_directory: directory path precedents
        :param total_file_to_process: amount of files to process
        :param cluster_size: amount of cluster to look for
        """

        self.claim_text = data_tuple[1]  # original sentence
        self.tfidf_matrix = data_tuple[0]  # sentence vector
        self.cluster_size = 100
        self.km = self.cluster()
        self.print("unlabeled_clusters")

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

    def print(self, file_name):
        f = open(file_name + ".txt", 'w')
        clusters = self.km.labels_.tolist()
        claim_cluster = [[] for i in range(self.cluster_size)]
        for i in range(len(clusters)):
            claim_cluster[clusters[i]].append(self.claim_text[i])

        for claim_list in claim_cluster:
            for claim in claim_list:
                f.write(claim)
                f.write("\n")
            f.write("\n\n========================================================================\n\n")
        f.close()
