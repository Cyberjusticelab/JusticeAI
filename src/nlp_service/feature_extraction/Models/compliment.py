from feature_extraction.GlobalVariables import regex

from feature_extraction.Models import Abstract_Model

'''
COMPLIMENT
---------------------------------------------
Noun with adjectives
'''


class Compliment(Abstract_Model.AbstractModel):
    def __init__(self):
        Abstract_Model.AbstractModel.__init__(self)
        self.__quantifier = None

    ##########################################
    # SET QUANTIFIER
    # ----------------------------------------
    # quantifier: string
    # tag: string
    def set_quantifier(self, quantifier, tag):
        if quantifier is not None:
            self.__quantifier = (quantifier, tag)
            self.add_tag_index(tag)

    ##########################################
    # GET QUANTIFIER
    def get_quantifier(self):
        return self.__quantifier

    ##########################################
    # ADD WORD
    # ----------------------------------------
    # word: String
    # tag: String
    def add_word(self, word, tag):
        if not (regex.Regex.key_word_match.match(tag)):
            return
        self._word.append((word, tag))
        self.add_tag_index(tag)

    def __str__(self):
        return "COMPLIMENT: " + str(self._word) + \
               " | Attribute: " + str(self._attribute) + \
               " | Quantifier: " + str(self.__quantifier)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        elif not (self.equal_lists(self.get_attribute(), other.get_attribute())):
            return False
        elif self.get_word() != other.get_word():
            return False
        elif self.get_quantifier() != other.get_quantifier():
            return False
        return True

    def empty_model(self):
        if len(self.get_word()) > 0:
            return False
        elif len(self.get_attribute()) > 0:
            return False
        elif self.get_quantifier() is not None:
            return False
        return True

    def __ne__(self, other):
        return not (self.__eq__(other))
