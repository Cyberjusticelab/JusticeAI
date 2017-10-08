from glove import Corpus, Glove
import itertools
import numpy
import pickle

class Word_Vectors:
    def __init__(self):
        self.word_set = r'/home/charmander/glove.42B.300d.txt'

    def load_glove_model_file(self, file):
        f = open(self.word_set, 'r')
        model = {}

        for line in range(100000):
            split_line = f.__next__().split()
            word = split_line[0]
            embedding = numpy.array([float(val) for val in split_line[1:]])
            model[word] = embedding
        f.close()
        return model

    @staticmethod
    def load_glove_model_pickle():
        with open('ser.pickle', 'rb') as pickle_file:
            model = pickle.load(pickle_file)
        return model

    def save_pickle(self, word_vectors):
        with open('ser.pickle', 'wb') as f:
            pickle.dump(word_vectors, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    word_vectors = Word_Vectors()
    model = word_vectors.load_glove_model_pickle()
    print(model['the'])