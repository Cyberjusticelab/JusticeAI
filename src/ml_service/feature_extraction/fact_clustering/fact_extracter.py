
from nltk.corpus import stopwords
from nltk.tokenize import ToktokTokenizer, sent_tokenize
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from pattern3.fr import singularize
import os
import re

np.seterr(all='raise')
stoppers = stopwords.words('french')
binaryFilePath = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../../non-lem.bin')

word_vectors = KeyedVectors.load_word2vec_format(binaryFilePath, binary=True)
tok = ToktokTokenizer()


def _extract(filename, errorWordSet):
    factDict = {}
    for line in _getFactsLinesFromFile(filename):
        for sentence in sent_tokenize(_clean(line)):
            vector = _vectorize(sentence, errorWordSet)
            if vector is not None:
                factDict[sentence] = vector
    return factDict


def _clean(line):
    return re.sub('\[\d+\]\s*', '',
                  line).strip().replace('\n', '').replace('\t', '')


def _getFactsLinesFromFile(filename):
    filePath = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), '../../../../text_bk/' + filename)
    normalizedFilePath = os.path.normpath(filePath)
    file = open(normalizedFilePath, encoding="ISO-8859-1")
    factMatch = re.compile('\[\d+\](.*\n){0,3}?(?=\[\d+\]|\n)', re.M)
    lines = file.read()
    file.close
    return factMatch.findall(lines)


def _vectorize(sentence, errorWordSet):
    vec = np.zeros(500)
    numWords = 0
    for words in tok.tokenize(sentence):
        for word in words.split('-'):
            word = word.lower().strip('.0123456789')
            if word not in stoppers:
                newWord = np.zeros(500)
                try:
                    newWord = word_vectors.wv[word]
                    numWords += 1
                    vec = np.add(vec, newWord)
                except:
                    try:
                        newWord = word_vectors.wv[singularize(word)]
                        numWords += 1
                        vec = np.add(vec, newWord)
                    except:
                        errorWordSet.add(word)
    if numWords < 1:
        return None
    return np.divide(vec, numWords)


def extractFactsFromFiles(j):
    errorWordSet = set()
    sentences = {}
    dirPath = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), '../../../../text_bk/')
    normalizedDataDir = os.path.normpath(dirPath)
    for i in os.listdir(normalizedDataDir):
        if 'AZ-51' in i and j > 0:
            j -= 1
            newSentences = _extract(i, errorWordSet)
            sentences.update(newSentences)
    _saveErrorWords(errorWordSet)
    return sentences


def _saveErrorWords(errorWordSet):
    filePath = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), '../../error_words.txt')
    normalizedFilePath = os.path.normpath(filePath)

    errorFile = open(normalizedFilePath, 'w')
    for err in errorWordSet:
        errorFile.write(err + '\n')
    errorFile.close()
