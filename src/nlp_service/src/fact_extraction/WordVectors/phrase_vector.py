import nltk.tokenize
import numpy
from numpy import dot
from numpy.linalg import norm
from src.fact_extraction.WordVectors import word_vector


class PhraseVector:
    def __init__(self):
        self.__model = word_vector.WordVectors().load_glove_model_pickle()

    ###############################################
    # COMPARE PHRASES
    # ---------------------------------------------
    # Compares sentences to a statement and returns
    # probability matrix that represents the
    # resemblance of phrases to the statement
    #
    # statement: list[word tokens]
    # phrase_set: list[list[word tokens]]
    def compare_phrases(self, statement, phrase_set):
        probability_matrix = numpy.empty(len(phrase_set))
        for i in range(len(phrase_set)):
            probability_matrix[i] = self.__similarities(statement, phrase_set[i])
        return probability_matrix

    ###############################################
    # SIMILARITIES
    # ---------------------------------------------
    # sum of every word vector in a phrase
    # compute cosine distance and return result in
    # numpy arrya
    #
    # a: word tokens
    # b: word tokens
    def __similarities(self, a, b):
        vector_a = numpy.zeros(300)
        vector_b = numpy.zeros(300)

        for words in a:
            key = remove_punctuation(words.lower())
            vector_a = numpy.add(vector_a, self.__model[key])

        for words in b:
            key = remove_punctuation(words.lower())
            vector_b = numpy.add(vector_b, self.__model[key])

        cos_sim = dot(vector_a, vector_b) / (norm(vector_a) * norm(vector_b))
        return cos_sim


###############################################
# REMOVE PUNCTUATION
# ---------------------------------------------
def remove_punctuation(sentence):
    new_str = sentence
    to_remove = ".?!\"\'"
    table = {ord(char): None for char in to_remove}
    return new_str.translate(table)


if __name__ == '__main__':
    question = nltk.word_tokenize(remove_punctuation("color car"))