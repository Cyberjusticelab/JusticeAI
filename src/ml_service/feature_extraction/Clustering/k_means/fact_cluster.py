import re
import nltk
import os
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from src.ml_service.feature_extraction.Preprocessing.Taimoor_Parser.fact_extraction import extract_data_from_cases
from src.ml_service.feature_extraction.Preprocessing.Taimoor_Parser.preprocessing import preprocessing
from src.ml_service.GlobalVariables.GlobalVariable import Global


class KMeansWrapper:
    def __init__(self, precedent_directory, total_file_to_process, cluster_size):
        """
        :param precedent_directory: directory path precedents
        :param total_file_to_process: amount of files to process
        :param cluster_size: amount of cluster to look for
        """
        raw_claim_text = extract_data_from_cases(precedent_directory, total_file_to_process)
        self.claim_text = preprocessing(raw_claim_text)
        self.tfidf_matrix = self.init_tfidf()
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

    def init_tfidf(self):
        # define vectorizer parameters
        tfidf_vectorizer = TfidfVectorizer(encoding="iso-8859-1",
                                           stop_words=stopwords.words('french'),
                                           strip_accents='ascii',
                                           use_idf=True,
                                           tokenizer=self.tokenize_and_stem,
                                           min_df=0.01, max_df=0.8, norm='l2',
                                           ngram_range={1, 4}
                                           )
        return tfidf_vectorizer.fit_transform(self.claim_text)

    def cluster(self):
        km = KMeans(n_clusters=self.cluster_size, init='k-means++')
        km.fit(self.tfidf_matrix)
        return km

    def print(self, file_name):
        f = open(file_name + ".txt", 'w')
        clusters = self.km.labels_.tolist()
        claim_cluster = [[] for i in range(self.cluster_size)]
        index = 0
        for claim in self.claim_text:
            claim_cluster[clusters[index]].append(claim)
            index += 1
        for claim_list in claim_cluster:
            for claim in claim_list:
                f.write(claim)
                f.write("\n")
            f.write("\n\n========================================================================\n\n")
        f.close()


if __name__ == '__main__':
    KMeansWrapper(os.path.normpath(Global.Precedence_Directory), 100, 100)
