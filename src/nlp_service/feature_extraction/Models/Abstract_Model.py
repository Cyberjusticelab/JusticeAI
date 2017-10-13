from feature_extraction.WordVectors.phrase_vector import PhraseVector
from feature_extraction.GlobalVariables.regex import Regex

'''
ABSTRACT MODEL
-----------------------------------------
'''


class AbstractModel:
    # we will need to train this to improve threshold
    match_threshold = 0.6

    #####################################
    # CONSTRUCTOR
    def __init__(self):
        self._word = []
        self._attribute = []
        self._tags = {}

    #####################################
    # GET WORD
    def get_word(self):
        return self._word

    #####################################
    # GET ATTRIBUTE
    def get_attribute(self):
        return self._attribute.copy()

    #####################################
    # ADD ATTRIBUTE
    def add_attribute(self, qualifier, tag):
        if qualifier is not None:
            self._attribute.append((qualifier, tag))
            self.add_tag_index(tag)

    #####################################
    # ADDS TAG INDEX
    # -----------------------------------
    # Adds a tag index to the dictionary
    # where the value is a list of
    # logical definitions
    # clause/predicate/compliment
    #
    # tag: string
    def add_tag_index(self, tag):
        try:
            model = self._tags[tag]
            self._tags[tag].append(self)
        except KeyError:
            self._tags[tag] = [self]

    #####################################
    # GET ELEMENT FROM TAG
    # -----------------------------------
    # returns value from dictionary
    #
    # tag: string
    # return: list[AbstractModel)
    def get_element_from_tag(self, tag):
        try:
            return self._tags[tag]
        except:
            return None

    #####################################
    # CATEGORY MATCH
    # -----------------------------------
    # Compares a category to the list of words
    # using word vectors
    #
    # Returns: True if match is above threshold
    def category_match(self, category):
        p = PhraseVector()
        for words in self._word:
            if Regex.relevant_word_match.match(words[1]):
                if p.compare_phrases([words[0]], [category]) > self.match_threshold:
                    return True
        return False

    #####################################
    # LIST EQUALITY
    @staticmethod
    def equal_lists(list1, list2):
        if len(list1) != len(list2):
            return False

        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return False
        return True
