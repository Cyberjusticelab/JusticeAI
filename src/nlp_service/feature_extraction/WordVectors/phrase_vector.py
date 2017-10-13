import nltk.tokenize
import numpy
from numpy import dot
from numpy.linalg import norm
from feature_extraction.WordVectors import word_vector


class PhraseVector:
    __v = word_vector.WordVectors()
    __model = __v.load_glove_model_pickle()
    __matrix_dimension = 300

    def __init__(self):
        pass

    ###############################################
    # COMPARE PHRASES
    # ---------------------------------------------
    # Compares sentences to a statement and returns
    # probability matrix that represents the
    # resemblance of phrases to the statement
    #
    # statement: list[word tokens]
    # phrase_set: list[list[word tokens]]
    def compare_phrases(self, statement, phrase):
        probability_matrix = self.__similarities(statement, phrase)
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
        vector_a = numpy.zeros(self.__matrix_dimension)
        vector_b = numpy.zeros(self.__matrix_dimension)

        for words in a:
            key = self.remove_punctuation(words.lower())
            vector_a = numpy.add(vector_a, self.__model[key])

        for words in b:
            key = self.remove_punctuation(words.lower())
            vector_b = numpy.add(vector_b, self.__model[key])

        cos_sim = dot(vector_a, vector_b) / (norm(vector_a) * norm(vector_b))
        return cos_sim

    ###############################################
    # REMOVE PUNCTUATION
    # ---------------------------------------------
    @staticmethod
    def remove_punctuation(sentence):
        new_str = sentence
        to_remove = ".?!\"\'"
        table = {ord(char): None for char in to_remove}
        return new_str.translate(table)


if __name__ == '__main__':
    question = nltk.word_tokenize("lease")
    phrase_set = nltk.word_tokenize("month")
    __v = PhraseVector()
    result = __v.compare_phrases(question, phrase_set)
    result = __v.compare_phrases(question, phrase_set)
    print(result)
