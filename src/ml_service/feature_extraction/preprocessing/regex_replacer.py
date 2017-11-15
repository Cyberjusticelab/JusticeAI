import re
import string
from word_vectors.vectors import FrenchVectors
from nltk.tokenize import word_tokenize
from nltk.tokenize.moses import MosesDetokenizer


class RegexReplacer():
    money_match = re.compile('\d+\s*?\$')
    date_match = re.compile('[\d[a-zA-Z]+\s]*[\d*\s*]*janvier\s*\d*|'
                            '[\d[a-zA-Z]+\s]*[\d*\s*]*février\s*\d*|'
                            '[\d[a-zA-Z]+\s]*[\d*\s*]*mars\s*\d*|'
                            '[\d[a-zA-Z]+\s]*[\d*\s*]*avril\s*\d*|'
                            '[\d[a-zA-Z]+\s]*[\d*\s*]*mai\s*\d*|'
                            '[\d[a-zA-Z]+\s]*[\d*\s*]*juin\s*\d*|'
                            '[\d[a-zA-Z]+\s]*[\d*\s*]*juillet\s*\d*|'
                            '[\d[a-zA-Z]+\s]*[\d*\s*]*août\s*\d*|'
                            '[\d[a-zA-Z]+\s]*[\d*\s*]*septembre\s*\d*|'
                            '[\d[a-zA-Z]+\s]*[\d*\s*]*octobre\s*\d*|'
                            '[\d[a-zA-Z]+\s]*[\d*\s*]*novembre\s*\d*|'
                            '[\d[a-zA-Z]+\s]*[\d*\s*]*décembre\s*\d*')
    apostrophe_match = re.compile('\w\'')
    unnecessary_white_space_match = re.compile("\s\s+")
    translator = str.maketrans('', '', string.punctuation)

    def __init__(self):
        pass

    @staticmethod
    def normalize_string(line):
        """
        Normalizes a string in order to reduce matrix dissimilarities
        between sentences that have the same contextual information
        1- Find and replace dates
        2- Find and replace money
        3- removes l', j', d' because python considers ['] as punctuation
           and was therefore creating weird strings
        4- Remove punctuation
        5- Removes unnecessary white spaces
        6- Tokenzie string and remove stop words
        7- remove remaining digits
        :param line: String
        :return: String
        """
        new_str = re.sub(RegexReplacer.money_match, ' argent', line)
        new_str = re.sub(RegexReplacer.date_match, ' date', new_str)
        new_str = re.sub(RegexReplacer.apostrophe_match, ' ', new_str)
        new_str = re.sub(RegexReplacer.unnecessary_white_space_match, " ", new_str)
        new_str = new_str.translate(RegexReplacer.translator)
        new_str = RegexReplacer.__remove_stop_words(new_str)
        new_str = ''.join([i for i in new_str if not i.isdigit()])
        try:
            if new_str[0] == " ":
                new_str = new_str[1:]
        except IndexError:
            return None
        return new_str

    @staticmethod
    def __remove_stop_words(line):
        """
        Remove stop words and order the list
        This creates even less dissimilarities between statements
        :param line: String
        :return: String
        """
        word_list = word_tokenize(line, 'french')
        filtered_words = []
        for word in word_list:
            if word in FrenchVectors.get_stop_tokens():
                continue
            else:
                filtered_words.append(word)
        filtered_words.sort()
        detokenizer = MosesDetokenizer()
        return detokenizer.detokenize(filtered_words, return_str=True)
