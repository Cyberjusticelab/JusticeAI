# -*- coding: utf-8 -*-
from textblob import TextBlob
import nltk
import random

class TenantLandlordClassifier(object):
    trainingData = [
        ('I am a tenant', 'tenant'),
        ('I am a payer', 'tenant'),
        ('I am a lodger', 'tenant'),
        ('I am a leaseholder', 'tenant'),
        ('tenant', 'tenant'),
        ('payer', 'tenant'),
        ('lodger', 'tenant'),
        ('leaseholder', 'tenant'),
        ('I am the tenant', 'tenant'),
        ('I am the payer', 'tenant'),
        ('I am the lodger', 'tenant'),
        ('I am the leaseholder', 'tenant'),
        ('I am a landlord', 'landlord'),
        ('I am a landlady', 'landlord'),
        ('landlord', 'landlord'),
        ('landlady', 'landlord'),
        ('I am a landowner', 'landlord'),
        ('I am a landlord', 'landlord'),
    ]
    random.shuffle(trainingData)
    vocab = set()

    """docstring for TenantLandlordClassifier"""
    def __init__(self):
        self.train()

    # Turns an N-gram or list of N-grams
    # into its vector representation
    def vectorize(self, elems):
        trainingElem = dict.fromkeys(TenantLandlordClassifier.vocab, False)
        print('-----------')
        print(elems)
        self.print_vector(trainingElem)
        if isinstance(elems, tuple):
            if elems in TenantLandlordClassifier.vocab:
                trainingElem[elems] = True
            else:
                trainingElem['UNKOWN'] = True
        else:
            for elem in elems:
                print(elem)
                if elem in TenantLandlordClassifier.vocab:
                    trainingElem[elem] = True
                else:
                    trainingElem['UNKOWN'] = True
        self.print_vector(trainingElem)
        print('===========')
        return trainingElem

    # Prints a vector. Useful for debugging.
    def print_vector(self, vector):
        output = "{"
        for key, value in vector.items():
            if value:
                output += str(key) + ","
        output += "}"
        print(output)

    def train(self):
        self.createVocabulary()
        cleanData = self.preprocessTrainingData()
        self.cl = nltk.classify.NaiveBayesClassifier.train(cleanData)

    # Creates a vocabulary set based on 3-grams
    def createVocabulary(self):
        for elem in self.trainingData:
            for grams in self.stemAndTrigramify(elem[0]):
                print(grams)
                TenantLandlordClassifier.vocab.add(grams)

    # An intermediat preprocessing step. Stemms each word
    # And splits them into trigrams
    def stemAndTrigramify(self, textString):
        text = TextBlob(textString.lower())
        words = text.words.stem()
        newWordList = []
        newWordList.append('<START>')
        newWordList.extend(words.stem())
        newWordList.append('<END>')
        return nltk.trigrams(newWordList)

    # Preprocesses the input training data
    def preprocessTrainingData(self):
        trainingList = []
        for elem in TenantLandlordClassifier.trainingData:
            for gram in self.stemAndTrigramify(elem[0]):
                data = (self.vectorize(gram), elem[1])
                trainingList.append(data)
        return trainingList

    def preprocessEvaluationString(self, evalString):
        self.stemAndTrigramify(evalString)

    def classify(self, textString):
        inputList = list(self.stemAndTrigramify(textString))
        vector = self.vectorize(inputList)
        return self.cl.prob_classify(vector)

a = TenantLandlordClassifier()
testData = [
    ('I am presently a landlord', 'landlord'),
    ('I am a tenant', 'tenant'),
    ('landlord', 'landlord'),
    ('I am presently a tenant', 'tenant')
]

for i in testData:
    result = a.classify(i[0])
    print(result.__dict__)
    print(i[0] + ": " + result.max() + " - " + i[1])
