from src.fact_extraction.WordVectors.phrase_vector import PhraseVector
from src.fact_extraction.GlobalVariables.regex import Regex


'''
ABSTRACT MODEL
-----------------------------------------
'''


class AbstractModel:
    # we will need to train this
    match_threshold = 0.6

    def __init__(self):
        self._word = []
        self._qualifier = []
        self._tags = {}

    def get_word(self):
        return self._word

    def get_qualifier(self):
        return self._qualifier.copy()

    def add_qualifier(self, qualifier, tag):
        if qualifier is not None:
            self._qualifier.append((qualifier, tag))
            self.add_tag_index(tag)

    def add_tag_index(self, tag):
        try:
            model = self._tags[tag]
            self._tags[tag].append(self)

        except:
            self._tags[tag] = [self]

    def get_element_from_tag(self, tag):
        try:
            return self._tags[tag]
        except:
            return None

    def category_match(self, category):
        p = PhraseVector()
        for words in self._word:
            if Regex.relevant_word_match.match(words[1]):
                if p.compare_phrases([words[0]], [category]) > self.match_threshold:
                    return True
        return False


    @staticmethod
    def equal_lists(list1, list2):
        if len(list1) != len(list2):
            return False

        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return False
        return True

if __name__ == '__main__':
    pass