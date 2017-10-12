from src.fact_extraction.Models import Abstract_Model
from src.fact_extraction.GlobalVariables import regex


'''
COMPLIMENT
---------------------------------------------
Noun with adjectives
'''


class compliment(Abstract_Model.AbstractModel):
    def __init__(self):
        Abstract_Model.AbstractModel.__init__(self)
        self.__quantifier = None

    def set_quantifier(self, quantifier, tag):
        if quantifier is not None:
            self.__quantifier = (quantifier, tag)
            self.add_tag_index(tag)

    def get_quantifier(self):
        return self.__quantifier
    
    def __str__(self):
        return "COMPLIMENT: " + str(self._word) + \
               " | Qualifier: " + str(self._qualifier) + \
               " | Quantifier: " + str(self.__quantifier)

    def set_word(self, word, tag):
        if not(regex.Regex.temp_match.match(tag)):
            return
        self._word.append((word, tag))
        self.add_tag_index(tag)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        elif not (self.equal_lists(self.get_qualifier(), other.get_qualifier())):
            return False
        elif self.get_word() != other.get_word():
            return False
        elif self.get_quantifier() != other.get_quantifier():
            return False
        return True

    def empty_model(self):
        if len(self.get_word()) > 0:
            return False
        elif len(self.get_qualifier()) > 0:
            return False
        elif self.get_quantifier() is not None:
            return False
        return True

    def __ne__(self, other):
        return not (self.__eq__(other))