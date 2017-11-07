import re

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

from src.ml_service.feature_extraction.Preprocessing.Taimoor_Parser.fact_extraction import extract_data_from_cases
from src.ml_service.feature_extraction.Preprocessing.Taimoor_Parser.preprocessing import preprocessing
from src.ml_service.GlobalVariables.GlobalVariable import Global

# stem words


def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return filtered_tokens


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


if __name__ == '__main__':
    stemmer = SnowballStemmer("french")

    claim_text = extract_data_from_cases(Global.Precedence_Directory, 5000)
    claim_text = preprocessing(claim_text)
    print("finished preprocessing")
    f = open(r'cluster_dir/clusters.txt', 'w')

    totalvocab_stemmed = []
    totalvocab_tokenized = []
    stopwords = stopwords.words('french')
    stopwords += ['moisDanslannee', 'pour ces motifs, le tribunal']

    for i in claim_text:
        allwords_stemmed = tokenize_and_stem(i)  # for each item in 'synopses', tokenize/stem
        allwords_stemmed = [word for word in allwords_stemmed if word not in stopwords]
        totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list

        allwords_tokenized = tokenize_only(i)
        allwords_tokenized = [word for word in allwords_tokenized if word not in stopwords]
        totalvocab_tokenized.extend(allwords_tokenized)

    # define vectorizer parameters
    tfidf_vectorizer = TfidfVectorizer(encoding="iso-8859-1",
                                       stop_words=stopwords,
                                       strip_accents='ascii',
                                       use_idf=True,
                                       tokenizer=tokenize_and_stem,
                                       min_df=0.01, max_df=0.8, norm='l2',
                                       ngram_range={1, 4}
                                       )

    tfidf_matrix = tfidf_vectorizer.fit_transform(claim_text)  # fit the vectorizer to synopses

    f.write(tfidf_vectorizer.get_feature_names().__str__())
    f.write("\n")
    from sklearn.cluster import KMeans

    km = KMeans(n_clusters=550, init='k-means++')
    km.fit(tfidf_matrix)

    clusters = km.labels_.tolist()

    print(clusters)
    print(len(claim_text))
    claim_cluster = [[] for i in range(550)]
    index = 0

    for claim in claim_text:
        claim_cluster[clusters[index]].append(claim)
        index += 1

    for claimlist in claim_cluster:
        for claim in claimlist:
            f.write(claim)
            f.write("\n")
        f.write("\n\n========================================================================\n\n")

    f.close()
