# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
from nltk.tokenize import ToktokTokenizer, sent_tokenize
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from pattern3.fr import singularize
import os
import re
import logging
import related_word_fetcher

logger = logging.getLogger('fact_clustering')
np.seterr(all='raise')
stoppers = stopwords.words('french')
binaryFilePath = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../../WordVectors/non-lem.bin')
binaryFilePath = os.path.normpath(binaryFilePath)
word_vectors = KeyedVectors.load_word2vec_format(binaryFilePath, binary=True)
tok = ToktokTokenizer()


def _extract(filename, errorWordSet):
    """
        Extracts all sentence vectors from given files
        filename: name of precedent to extract facts from
        errorWordSet: set of all error words (not found in vector model). Adds
                      new error words to it
        returns a dictionary with keys as sentence string, and values as vectors
    """
    factDict = {}
    for line in _getFactsLinesFromFile(filename):
        for sentence in re.split(',;.?!', _clean(line)):
            vector = _vectorize(sentence, errorWordSet)
            if vector is not None:
                factDict[sentence] = vector
    return factDict


def _clean(line):
    return re.sub('\[\d+\]\s*', '',
                  line).strip().replace('\n', '').replace('\t', '')


def _getFactsLinesFromFile(filename):
    """
        Get all facts from the given file, and returns them
        filename: name of precedent file
        returns: all facts within that precedent
    """
    filePath = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), '../../../../text_bk/' + filename)
    normalizedFilePath = os.path.normpath(filePath)
    file = open(normalizedFilePath, encoding="ISO-8859-1")
    factMatch = re.compile('\[\d+\](.*\n){0,3}?(?=\[\d+\]|POUR CE)', re.M)
    lines = file.read()
    file.close()
    intermed = re.compile("(D É C I S I O N|DÉCISION)").split(lines)
    if len(intermed) < 3:
        return []
    intermed = intermed[2].split("MOTIFS, LE TRIBUNAL :")
    if len(intermed) < 2:
        return []
    lines = intermed[0]
    return factMatch.findall(lines)


def _vectorize(sentence, errorWordSet):
    """
        Vectorizes the given sentence string
        sentence: string of words to vectorize
        errorWordSet: set of error words. adds words that are
                      not found.
        returns: the average vector associated with the sentence
                 or None if all words are not found
    """
    vec = np.zeros(500)
    numWords = 0
    for words in tok.tokenize(sentence):
        for word in words.split('-'):
            word = word.lower()
            wordRegex = re.compile('[A-zÀ-ÿ]+')
            wordMatch = wordRegex.search(word)
            if wordMatch is None:
                continue
            word = wordMatch.group()
            if word not in stoppers:
                newWord = np.zeros(500)
                try:
                    newWord = word_vectors[word]
                    numWords += 1
                    vec = np.add(vec, newWord)
                except BaseException:
                    similarWord = related_word_fetcher.find_related(word)
                    try:
                        newWord = word_vectors[similarWord]
                        logger.info("Using similar word: " +
                                    word + " - " + similarWord)
                        numWords += 1
                        vec = np.add(vec, newWord)
                    except BaseException:
                        singularized = singularize(word)
                        if singularized in word_vectors:
                            newWord = word_vectors[singularized]
                            logger.info("Using singularization")
                            numWords += 1
                            vec = np.add(vec, newWord)
                        else:
                            errorWordSet.add(word)
    if numWords < 1:
        return None
    return np.divide(vec, numWords)


def extractFactsFromFiles(j):
    """
        Extracts all facts from the given number of files
        j: number of file to extract facts from
        returns a dictionary with keys as sentence string, and values as vectors
    """
    errorWordSet = set()
    sentences = {}
    dirPath = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), '../../../../text_bk/')
    normalizedDataDir = os.path.normpath(dirPath)
    for i in os.listdir(normalizedDataDir):
        if 'AZ-51' in i and j > 0:
            logger.info("Extracting file: " + i)
            j -= 1
            newSentences = _extract(i, errorWordSet)
            sentences.update(newSentences)
    _saveErrorWords(errorWordSet)
    return sentences


def _saveErrorWords(errorWordSet):
    """
        Saves all given error words to a file
        errorWordSet: set of error words
    """
    filePath = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), '../../error_words.txt')
    normalizedFilePath = os.path.normpath(filePath)

    errorFile = open(normalizedFilePath, 'w', encoding="ISO-8859-1")
    for err in errorWordSet:
        errorFile.write(err + '\n')
    errorFile.close()
