# -*- coding: utf-8 -*-
from stanfordcorenlp import StanfordCoreNLP
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords
import re

#t = Tree.fromstring(nlp.parse(sentence))

def extract(filename):
    returnList = []
    file = open(r'C:/Users/bulbasaur/Desktop/text_bk/' + filename, 'r', encoding="ISO-8859-1")
    factMatch = re.compile('\[\d+\]')
    decision = False
    for lines in file:
        if 'POUR CES MOTIFS' in lines:
            decision = True

        elif factMatch.match(lines):
            num = factMatch.match(lines).group(0)
            index = num.replace('[', "")
            index = index.replace(']', "")
            if decision:
                if (int(index) == 1):
                    decision = False
                else:
                    continue

            sentence = lines.replace(num, "").lower()
            sentence = sentence.replace('\n', "")
            sentence = ner(sentence)
            returnList.append(sentence)

    file.close()
    return returnList

def ner(sentence):
    moneyMatch = re.compile('(\d*\s*\$)')
    if moneyMatch.search(sentence):
        sentence = re.sub('[\d*\s*]*\$', ' argent', sentence)
    return sentence

def key_words(nlp, sentence):
    word_list = nlp.word_tokenize(sentence)
    stemmer = FrenchStemmer()
    more_words = [',', ';', '.', '!', '?', 'le', 'la', "l'", "d'", 'les', 'plus', 'dû', 'considérant']
    stop_words = stopwords.words('french') + more_words
    key_lst = []
    for i in word_list:
        if i.lower() in stop_words:
            pass
        else:
            key_lst.append(stemmer.stem(i))
    return key_lst

dir = r'C:\Users\bulbasaur\Desktop\text_bk'
nlp = StanfordCoreNLP(r'C:\Users\bulbasaur\Desktop\stanford-corenlp-full-2017-06-09', lang='fr')
s = extract('AZ-51115100.txt')
for e in s:
    print(key_words(nlp, e))