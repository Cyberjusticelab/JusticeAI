# -*- coding: utf-8 -*-
# flake8: noqa
##
# Utility script used to install required NLTK modules
# and augment the input set with synonyms.
##

import os

import nltk

# from bllipparser.ModelFetcher import download_and_install_model

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
# model_dir = download_and_install_model('WSJ', '/tmp/models')

from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from Archive.services import TenantLandlordClassifier
from Archive.services import ProblemCategoryClassifier
from Archive.services import HasLeaseExpiredClassifier
from Archive.services import IsHabitableClassifier
from Archive.services import IsStudentClassifier
from Archive.services import IsTenantDeadClassifier
from Archive.services import LeaseTermTypeClassifier


def expandInputFile(inputFile, outputFile):
    f = open(inputFile)
    samples = set([l.strip('\n') for l in f.readlines()])
    f.close()

    expanded = set()
    stoppers = set(stopwords.words('english'))
    print(inputFile.strip(os.getcwd() + '/old_data/') +
          ' old size: ' + str(len(samples)))
    while len(expanded) != len(samples):
        for sample in samples:
            sample = sample.lower()
            words = nltk.word_tokenize(sample)
            for i in words:
                if i not in stoppers:
                    synsets = wn.synsets(i)
                    commons = set([synset.name().split(".")[0]
                                   for synset in synsets])
                    if len(commons) > 0:
                        for hyponym in commons:
                            newSample = sample.replace(
                                i, hyponym.replace("_", " "))
                            expanded.add(newSample)
        samples = expanded.copy()

    print(outputFile.strip(os.getcwd() + '/old_data/') +
          ' new size: ' + str(len(expanded)))

    out = open(outputFile, 'w')
    for item in expanded:
        out.write(item + '\n')
    out.close()


def trainClassifiers():
    TenantLandlordClassifier(True)
    ProblemCategoryClassifier(True)
    HasLeaseExpiredClassifier(True)
    IsHabitableClassifier(True)
    IsStudentClassifier(True)
    IsTenantDeadClassifier(True)
    LeaseTermTypeClassifier(True)


for directory in os.listdir(os.getcwd() + '/old_data'):
    for file in os.listdir(os.getcwd() + '/old_data/' + directory):
        if '.txt' in file and '.extended.txt' not in file:
            inputFile = os.getcwd() + '/old_data/' + directory + '/' + file
            outputFile = os.getcwd() + '/old_data/' + directory + '/' + \
                file.split('.')[0] + '.extended.txt'
            expandInputFile(inputFile, outputFile)
trainClassifiers()
