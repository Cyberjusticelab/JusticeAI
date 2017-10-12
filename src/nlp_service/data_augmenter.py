##
# Utility script used to augment the input set with synonyms.
##

from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import nltk
import os


def expandInputFile(inputFile, outputFile):
    f = open(inputFile)
    samples = set([l.strip('\n') for l in f.readlines()])

    expanded = set()
    stoppers = set(stopwords.words('english'))
    print(inputFile.strip('data/') + ' old size: ' + str(len(samples)))
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

    print(outputFile.strip('data/') + ' new size: ' + str(len(expanded)))

    out = open(outputFile, 'w')
    for item in expanded:
        out.write(item + '\n')


for directory in os.listdir('data'):
    for file in os.listdir('data/' + directory):
        inputFile = 'data/' + directory + '/' + file
        outputFile = 'data/' + directory + '/' + \
            file.split('.')[0] + '.extended.txt'
        expandInputFile(inputFile, outputFile)
