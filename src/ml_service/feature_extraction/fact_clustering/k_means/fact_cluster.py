import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from fact_extraction import extract_data_from_cases
from stop_words import get_stop_words
from preprocessing import preprocessing

stemmer = SnowballStemmer("french")

claim_text = extract_data_from_cases('/Users/taimoorrana/Downloads/text_bk/', 1000)
claim_text = preprocessing(claim_text)
f = open('helloworld.txt', 'w')

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
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


# not super pythonic, no, not at all.
# use extend so it's a big flat list of vocab
totalvocab_stemmed = []
totalvocab_tokenized = []
# stopwords = stopwords.words('french')
stopwords = get_stop_words('fr')
# for word in stopwords:
#     print(word)
for i in claim_text:
    allwords_stemmed = tokenize_and_stem(i)  # for each item in 'synopses', tokenize/stem
    allwords_stemmed = [word for word in allwords_stemmed if word not in stopwords]
    totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list

    allwords_tokenized = tokenize_only(i)
    allwords_tokenized = [word for word in allwords_tokenized if word not in stopwords]
    totalvocab_tokenized.extend(allwords_tokenized)

from sklearn.feature_extraction.text import TfidfVectorizer

# define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(encoding="iso-8859-1", max_features=200000,
                                   stop_words=stopwords,
                                   use_idf=True, tokenizer=tokenize_and_stem)

tfidf_matrix = tfidf_vectorizer.fit_transform(claim_text)  # fit the vectorizer to synopses

f.write(tfidf_vectorizer.get_feature_names().__str__())
f.write("\n")

from sklearn.metrics.pairwise import cosine_similarity

dist = 1 - cosine_similarity(tfidf_matrix)

from sklearn.cluster import KMeans

km = KMeans(n_clusters=10, init='k-means++')
km.fit(tfidf_matrix)

# import matplotlib.pyplot as plt
# wcss = []
# for i in range(1,30):
#     km = KMeans(n_clusters=i, init='k-means++')
#     km.fit(tfidf_matrix)
#     print(i)
#     wcss.append(km.inertia_)
#
# plt.plot(range(1,30), wcss)
# plt.xlabel('numbers of cluster')
# plt.ylabel('wcss')
# plt.show()

clusters = km.labels_.tolist()

print(clusters)
print(len(claim_text))
claim_cluster = [[] for i in range(10)]
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
