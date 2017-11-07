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
from services.classifiers.tenant_landlord_classifier import TenantLandlordClassifier
from services.classifiers.problem_category_classifier import ProblemCategoryClassifier
from services.classifiers.has_lease_expired_classifier import HasLeaseExpiredClassifier
from services.classifiers.is_habitable_classifier import IsHabitableClassifier
from services.classifiers.is_student_classifier import IsStudentClassifier
from services.classifiers.is_tenant_dead_classifier import IsTenantDeadClassifier
from services.classifiers.lease_term_type_classifier import LeaseTermTypeClassifier


def expandInputFile(inputFile, outputFile):
    f = open(inputFile)
    samples = set([l.strip('\n') for l in f.readlines()])
    f.close()

    expanded = set()
    stoppers = set(stopwords.words('english'))
    print(inputFile.strip(os.getcwd() + '/data/') +
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

    print(outputFile.strip(os.getcwd() + '/data/') +
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


for directory in os.listdir(os.getcwd() + '/data'):
    for file in os.listdir(os.getcwd() + '/data/' + directory):
        if '.txt' in file and '.extended.txt' not in file:
            inputFile = os.getcwd() + '/data/' + directory + '/' + file
            outputFile = os.getcwd() + '/data/' + directory + '/' + \
                file.split('.')[0] + '.extended.txt'
            expandInputFile(inputFile, outputFile)
trainClassifiers()
