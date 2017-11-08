# -*- coding: utf-8 -*-
import os
import pickle
import random
import re
import time

import nltk
from nltk.corpus import stopwords
from textblob import TextBlob

dataPath = '/gram_classify/data/'


class GramClassifier(object):
    stopWords = set(stopwords.words('english'))
    stopWords.remove('not')
    stopWords.add('<START>')
    stopWords.add('<END>')
    months = ['january', 'february', 'march',
              'april', 'may', 'june',
              'july', 'august', 'september',
              'october', 'november', 'december']
    monthStem = [TextBlob(month).words.stem()[0] for month in months]

    """GramClassifier is a Naive Bayes Classifier
    which uses a combination of 3-gram, 2-gram and
    non stopwords in a vector to determine the class
    of the given input"""

    def __init__(self, baseName, inputFiles, forceTrain):
        if os.path.exists(os.getcwd() + dataPath + baseName + '/' + baseName + '.pickle') \
                and not forceTrain:
            self.createFromPickle(baseName, inputFiles)
        else:
            self.createFromTraining(baseName, inputFiles)

    def createFromTraining(self, baseName, inputFiles):
        print('==== Creating ' + self.__class__.__name__ + ' ====')
        startTime = time.time()
        self.loadData(baseName, inputFiles)
        random.shuffle(self.trainingData)
        self.vocab = set()
        self.train()
        elapsed = int(time.time() - startTime)
        print('==== Completed ' + self.__class__.__name__ +
              ' creation. Took ' + str(elapsed) + ' seconds ====')
        f = open(os.getcwd() + dataPath + baseName +
                 '/' + baseName + '.pickle', 'wb')
        pickle.dump(self.cl, f)
        f.close()

    def createFromPickle(self, baseName, inputFiles):
        print('=== Using Pickle version of ' +
              self.__class__.__name__ + ' ===')
        f = open(os.getcwd() + dataPath + baseName +
                 '/' + baseName + '.pickle', 'rb')
        self.cl = pickle.load(f)
        f.close()
        self.loadData(baseName, inputFiles)
        random.shuffle(self.trainingData)
        self.vocab = set()
        self.createVocabulary()

        # Loads data from from the given array
        # of input class names. e.g.:
        #
        # Input: ['class']
        #
        # Will load data from data/class.extended.txt and
        # treate them as examples of the 'class' category

    def loadData(self, baseName, inputFiles):
        self.trainingData = []
        for inp in inputFiles:
            f = open(os.getcwd() + dataPath + baseName +
                     '/' + inp + '.extended.txt')
            inputSet = set([l.strip('\n') for l in f.readlines()])
            inputTuples = []
            for inputString in inputSet:
                inputTuples.append((inputString, inp))
            self.trainingData.extend(inputTuples)

    # Turns an N-gram or list of N-grams
    # into its vector representation
    def vectorize(self, elems):
        trainingElem = dict.fromkeys(self.vocab, False)
        if isinstance(elems, tuple):
            if elems in self.vocab:
                trainingElem[elems] = True
            else:
                trainingElem['UNKOWN'] = True
        else:
            for elem in elems:
                if elem in self.vocab:
                    trainingElem[elem] = True
                else:
                    trainingElem['UNKOWN'] = True
        return trainingElem

    # Prints a vector. Useful for debugging.
    def print_vector(self, vector):
        output = "{"
        for key, value in vector.items():
            if value:
                output += str(key) + ","
        output += "}"
        print(output)

    # Creates the vocabulary based on the input files
    # and trains the classifier.
    def train(self):
        self.createVocabulary()
        cleanData = self.preprocessTrainingData()
        self.cl = nltk.classify.NaiveBayesClassifier.train(cleanData)

    # Creates a vocabulary set based on 3-grams
    def createVocabulary(self):
        for elem in self.trainingData:
            for grams in self.preprocess(elem[0]):
                self.vocab.add(grams)

    # An intermediate preprocessing step. Stems each word
    # Splits them into 3-grams, 2-grams and single words
    # that are not stopwords
    def preprocess(self, textString):
        text = TextBlob(textString.lower())
        words = text.words.stem()
        words = [self.preprocessDigits(word)
                 for word in words]
        words = [self.preprocessMonths(word)
                 for word in words]
        newWordList = []
        newWordList.append('<START>')
        newWordList.extend(words)
        newWordList.append('<END>')
        grams = [gram for gram in nltk.trigrams(
            newWordList) if len(set(gram) - self.stopWords) > 0]
        grams.extend([gram for gram in nltk.bigrams(newWordList)
                      if len(set(gram) - self.stopWords) > 0])
        grams.extend([word for word in words
                      if word not in self.stopWords])
        return grams

    def preprocessDigits(self, testString):
        if re.match('\d+\S*', testString):
            return '<DIGIT>'
        return testString

    def preprocessMonths(self, testString):
        if testString in self.monthStem:
            return '<MONTH>'
        else:
            return testString

    # Preprocesses the input training data
    def preprocessTrainingData(self):
        trainingList = []
        for elem in self.trainingData:
            for gram in self.preprocess(elem[0]):
                data = (self.vectorize(gram), elem[1])
                trainingList.append(data)
        return trainingList

    # Classifies the given text string into
    # one of the trained catigories. Returns the
    # highest classification category.
    def classify(self, textString):
        inputList = list(self.preprocess(textString))
        vector = self.vectorize(inputList)
        return self.cl.classify(vector)
