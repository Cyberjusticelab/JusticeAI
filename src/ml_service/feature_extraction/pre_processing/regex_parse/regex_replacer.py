import re
import string
from nltk.tokenize import word_tokenize
from nltk.tokenize.moses import MosesDetokenizer

from feature_extraction.pre_processing.word_vector.french_vector import FrenchVector

class RegexReplacer():

    money_match = re.compile(r'\b(\d{1,3}(\s\d{3}|,\d{2})*)+(\$|\s\$)')
    date_match = re.compile('(\d+?\w*?\s+?|)(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s+\d{2,4}|)')
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
        word_list = set(word_list)
        filtered_words = []
        for word in word_list:
            if word in FrenchVector.get_stop_tokens():
                continue
            else:
                filtered_words.append(word)
        filtered_words.sort()
        detokenizer = MosesDetokenizer()
        return detokenizer.detokenize(filtered_words, return_str=True)
