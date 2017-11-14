import re
import string


class RegexReplacer():
    money_match = re.compile('[\d*\s*,*]*\$')
    date_match = re.compile('[1er]*[\d*\s*]*janvier\s*\d*|'
                            '[1er]*[\d*\s*]*février\s*\d*|'
                            '[1er]*[\d*\s*]*mars\s*\d*|'
                            '[1er]*[\d*\s*]*avril\s*\d*|'
                            '[1er]*[\d*\s*]*mai\s*\d*|'
                            '[1er]*[\d*\s*]*juin\s*\d*|'
                            '[1er]*[\d*\s*]*juillet\s*\d*|'
                            '[1er]*[\d*\s*]*août\s*\d*|'
                            '[1er]*[\d*\s*]*septembre\s*\d*|'
                            '[1er]*[\d*\s*]*octobre\s*\d*|'
                            '[1er]*[\d*\s*]*novembre\s*\d*|'
                            '[1er]*[\d*\s*]*décembre\s*\d*')
    apostrophe_match = re.compile('\w\'')
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
        :param line: String
        :return: String
        """
        new_str = re.sub(RegexReplacer.money_match, ' argent', line)
        new_str = re.sub(RegexReplacer.date_match, ' date', new_str)
        new_str = re.sub(RegexReplacer.apostrophe_match, ' ', new_str)
        new_str = re.sub("\s\s+", " ", new_str)
        new_str = new_str.translate(RegexReplacer.translator)
        try:
            if new_str[0] == " ":
                new_str = new_str[1:]
        except IndexError:
            return None
        return new_str
