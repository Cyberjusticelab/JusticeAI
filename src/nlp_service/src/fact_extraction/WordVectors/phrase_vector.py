import nltk.tokenize
import numpy
from numpy import dot
from numpy.linalg import norm

from src.fact_extraction import word_vector
from src.fact_extraction.FactTree import sentence_pipeline
from src.fact_extraction.WordVectors import word_vector


class PhraseVector:
    def __init__(self):
        self.model = word_vector.Word_Vectors().load_glove_model_pickle()

    def compare_phrases(self, statement, phrase_set):
        probability_matrix = numpy.empty(len(phrase_set))

        for i in range(len(phrase_set)):
            probability_matrix[i] = self.similarities(statement, phrase_set[i])

        return probability_matrix

    def similarities(self, a, b):
        vector_a = numpy.zeros(300)
        vector_b = numpy.zeros(300)

        for words in a:
            key = remove_punctuation(words.lower())
            vector_a = numpy.add(vector_a, self.model[key])

        for words in b:
            key = remove_punctuation(words.lower())
            vector_b = numpy.add(vector_b, self.model[key])

        cos_sim = dot(vector_a, vector_b) / (norm(vector_a) * norm(vector_b))
        return cos_sim


def remove_punctuation(sentence):
    str = sentence
    to_remove = ".?!\"\'"
    table = {ord(char): None for char in to_remove}
    return str.translate(table)

if __name__ == '__main__':
    pv = PhraseVector()
    pipe = sentence_pipeline.Pipeline()
    pipe.pipe("color car red")
    question = nltk.word_tokenize(remove_punctuation("What is the color of you car"))
    print(pv.compare_phrases(question, pipe.get_raw_sent()))

    pipe.pipe("son hospital.")
    question = nltk.word_tokenize(remove_punctuation("color car"))
    print(pv.compare_phrases(question, pipe.get_raw_sent()))