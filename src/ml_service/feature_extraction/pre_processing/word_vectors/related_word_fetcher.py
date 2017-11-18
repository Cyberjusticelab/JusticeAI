import logging
import os
import pickle
import re
from urllib import request, parse

from bs4 import BeautifulSoup

from util.file import Log
from util.constant import Path

"""
This python module is used to fill in missing keys from the
word vector model. This script attempts to find the closest
similar word to the one given. The end goal will enable every
word to be vectorized.
"""

logger = logging.getLogger('fact_clustering')
verbeRegex = re.compile("(?<=Conjugaison du verbe )\S+")

"""
Cache is a dictionary which stores keys<words not found>
and maps them to values<words found>
"""

cache = {}
cachePickleFilePath = os.path.join(Path.cache_directory, r'cache.pickle')

# load pickle if it exists
if os.path.isfile(cachePickleFilePath):
    Log.write('Loading cached Pickle of words.')
    cacheFile = open(cachePickleFilePath, "rb")
    cache = pickle.load(cacheFile)


def _find_synonym(soup):
    """
    Finds a synonym to a word
    :param soup: BeautifulSoup
    :return: String if word found else None
    """
    node = soup.find(id="Synonymes")
    if node is None:
        return None
    synonyms = node.parent.next_sibling.next_sibling.text.split('\n')

    synonyms = [word for word in synonyms if word != '']
    return synonyms[0]


def _find_plural(soup):
    """
    Finds plural of given word
    :param soup: BeautifulSoup
    :return: String if word found else None
    """
    node = soup.find('i', string="Pluriel de")
    if node is None:
        return None
    return node.next_sibling.next_sibling.text


def _find_fem_plural(soup):
    """
    Finds feminine plural of word
    :param soup: BeautifulSoup
    :return: String if word found else None
    """
    node = soup.find('i', string="Féminin pluriel de")
    if node is None:
        return None
    return node.next_sibling.next_sibling.text


def _find_feminin(soup):
    """
    Finds feminine of word
    :param soup: BeautifulSoup
    :return: String if word found else None
    """
    node = soup.find('i', string="Féminin de")
    if node is None:
        return None
    return node.next_sibling.next_sibling.text


def _find_conjugation(soup):
    """
    Finds conjugation of verb
    :param soup: BeautifulSoup
    :return: String if word found else None
    """
    verbText = verbeRegex.search(soup.text)
    if verbText is None:
        return None
    return verbeRegex.search(soup.text).group()


def find_related(queryWord):
    """
    Returns a related word to the given word, using French
        Wikitionary. Returns the infinitif of verbs, the
        masculin singulier of nouns, or synonym.
    queryWord: word to lookup in wikitionary
    returns: a string containing the similar word, or None
             if none is found.
    """
    if queryWord in cache:
        return cache[queryWord]
    requestURL = u"https://fr.wiktionary.org/wiki/" + \
        parse.quote(queryWord)
    try:
        response = request.urlopen(requestURL)
    except BaseException:
        cache[queryWord] = None
        return None
    soup = BeautifulSoup(response, 'html.parser')

    relatedWord = _find_synonym(soup)
    if relatedWord is not None:
        cache[queryWord] = relatedWord
        return relatedWord

    relatedWord = _find_plural(soup)
    if relatedWord is not None:
        cache[queryWord] = relatedWord
        return relatedWord

    relatedWord = _find_fem_plural(soup)
    if relatedWord is not None:
        cache[queryWord] = relatedWord
        return relatedWord

    relatedWord = _find_feminin(soup)
    if relatedWord is not None:
        cache[queryWord] = relatedWord
        return relatedWord

    relatedWord = _find_conjugation(soup)
    if relatedWord is not None:
        cache[queryWord] = relatedWord
        return relatedWord

    cache[queryWord] = None
    return None


def save_cache():
    """
    Save cache of replaced words. This speeds up the process
    whenever a previously found word needs to be found again.
    :return: None
    """

    Log.write('Saving Pickle of cached words.')
    file = open(cachePickleFilePath, 'wb')
    pickle.dump(cache, file)
