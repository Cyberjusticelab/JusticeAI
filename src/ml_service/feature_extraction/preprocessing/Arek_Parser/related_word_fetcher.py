from bs4 import BeautifulSoup
from urllib import request, parse
import re
import logging
import pickle
import os
logger = logging.getLogger('fact_clustering')
verbeRegex = re.compile("(?<=Conjugaison du verbe )\S+")

cache = {}
__script_dir = os.path.abspath(__file__ + r"/../../../../")
__rel_path = r'word_vectors/cache.pickle'
cachePickleFilePath = os.path.join(__script_dir, __rel_path)
if os.path.isfile(cachePickleFilePath):
    print('Loading cached Pickle of words.')
    cacheFile = open(cachePickleFilePath, "rb")
    cache = pickle.load(cacheFile)


def _find_synonym(soup):
    node = soup.find(id="Synonymes")
    if node is None:
        return None
    synonyms = node.parent.next_sibling.next_sibling.text.split('\n')

    synonyms = [word for word in synonyms if word != '']
    return synonyms[0]


def _find_plural(soup):
    node = soup.find('i', string="Pluriel de")
    if node is None:
        return None
    return node.next_sibling.next_sibling.text


def _find_fem_plural(soup):
    node = soup.find('i', string="Féminin pluriel de")
    if node is None:
        return None
    return node.next_sibling.next_sibling.text


def _find_feminin(soup):
    node = soup.find('i', string="Féminin de")
    if node is None:
        return None
    return node.next_sibling.next_sibling.text


def _find_conjugation(soup):
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
        logger.info("Querying Wikitionary: " + requestURL)
        response = request.urlopen(requestURL)
    except BaseException:
        logger.info(requestURL + " not found.")
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


def find_errors():
    f = open('error_words.txt', 'r', encoding="ISO-8859-1")

    notFound = 0
    found = 0
    for i in f:
        i = i.strip('\n')
        related = find_related(i)
        if related is not None:
            logger.info(i + " : " + related)
            found += 1
        else:
            notFound += 1

    logger.info("Found: " + str(found))
    logger.info("Not Found: " + str(notFound))


def save_cache():
    __script_dir = os.path.abspath(__file__ + r"/../../../../")
    __rel_path = r'word_vectors/cache.pickle'
    path = os.path.join(__script_dir, __rel_path)
    logger.info('Saving Pickle of cached words.')
    file = open(path, 'wb')
    pickle.dump(cache, file)
