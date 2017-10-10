import numpy
import pickle


class WordVectors:
    def __init__(self):
        pass

    #####################################
    # LOAD MODEL FROM FILE
    def load_glove_model_file(self, file):
        f = open(file, 'r')
        model = {}

        for line in range(100000):
            split_line = f.__next__().split()
            word = split_line[0]
            embedding = numpy.array([float(val) for val in split_line[1:]])
            model[word] = embedding
        f.close()
        return model

    #####################################
    # LOAD MODEL FROM PICKLE
    @staticmethod
    def load_glove_model_pickle():
        with open('ser.pickle', 'rb') as pickle_file:
            model = pickle.load(pickle_file)
        return model

    #####################################
    # SAVE PICKLE
    def save_pickle(self, word_vectors):
        with open('ser.pickle', 'wb') as f:
            pickle.dump(word_vectors, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    word_vectors = WordVectors()
    model = word_vectors.load_glove_model_pickle()
    print(model['the'])