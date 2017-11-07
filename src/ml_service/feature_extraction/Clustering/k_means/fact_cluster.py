import re
import nltk
import os
import numpy
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from src.ml_service.feature_extraction.Preprocessing.Taimoor_Parser.fact_extraction import extract_data_from_cases
from src.ml_service.feature_extraction.Preprocessing.Taimoor_Parser.preprocessing import preprocessing
from src.ml_service.GlobalVariables.GlobalVariable import Global
from src.ml_service.feature_extraction.Preprocessing.Sam_Parser.PrecedenceParse import FrenchVectors


class KMeansWrapper:
    def __init__(self, precedent_directory, total_file_to_process, cluster_size):
        """
        :param precedent_directory: directory path precedents
        :param total_file_to_process: amount of files to process
        :param cluster_size: amount of cluster to look for
        """
        raw_claim_text = extract_data_from_cases(precedent_directory, total_file_to_process)
        self.claim_text = preprocessing(raw_claim_text)
        self.data_matrix = self.create_data_matrix()
        self.cluster_size = cluster_size
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

    def create_data_matrix(self):
        # define vectorizer parameters
        tfidf_vectorizer = TfidfVectorizer(encoding="iso-8859-1",
                                           stop_words=stopwords.words('french'),
                                           strip_accents='ascii',
                                           use_idf=True,
                                           tokenizer=self.tokenize_only,
                                           min_df=0.0, max_df=0.8, norm='l2',
                                           )

        tfidf_vectorizer.fit_transform(self.claim_text)
        word_idf_dict = dict(zip(tfidf_vectorizer.get_feature_names(), tfidf_vectorizer.idf_))
        FrenchVectors.word_idf_dict = word_idf_dict
        claim_vec_list = []
        for claim in self.claim_text:
            claim_vec_list.append(FrenchVectors.vectorize_sent(self.tokenize_only(claim)))
        return numpy.array(claim_vec_list)

    def cluster(self):
        km = KMeans(n_clusters=self.cluster_size, init='k-means++')
        km.fit(self.data_matrix)
        return km

    def print(self, file_name):
        f = open(file_name + ".txt", 'w')
        clusters = self.km.labels_.tolist()
        claim_cluster = [[] for i in range(self.cluster_size)]
        print("cluster size: ", len(clusters))
        print("claim_text size: ", len(self.claim_text))
        for i in range(len(clusters)):
            claim_cluster[clusters[i]].append(self.claim_text[i])

        for claim_list in claim_cluster:
            for claim in claim_list:
                f.write(claim)
                f.write("\n")
            f.write("\n\n========================================================================\n\n")


if __name__ == '__main__':
    KMeansWrapper(os.path.normpath(Global.Precedence_Directory), 100, 10)
