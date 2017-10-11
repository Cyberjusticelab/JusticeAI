from src.fact_extraction.Models import Abstract_Model
from src.fact_extraction.GlobalVariables import regex


'''
CLAUSE
-----------------------------------------------
Noun with verbs
'''


class Clause(Abstract_Model.AbstractModel):
    def __init__(self):
        Abstract_Model.AbstractModel.__init__(self)
        self.__quantifier = None

    def set_quantifier(self, quantifier):
        if quantifier is not None:
            self.__quantifier = quantifier

    def get_quantifier(self):
        return self.__quantifier

    def __str__(self):
        return "CLAUSE: " + str(self._word) + \
               " | Qualifier: " + str(self._qualifier) + \
               " | Quantifier: " + str(self.__quantifier)

    def set_word(self, word, tag = None):
        if tag is not None:
            if not(regex.Regex.temp_match.match(tag)):
                return
        if self._word is None:
            self._word = word
        else:
            self._word += ", " + word

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        elif not(self.equal_lists(self.get_qualifier(), other.get_qualifier())):
            return False
        elif self.get_word() != other.get_word():
            return False
        elif self.get_quantifier() != other.get_quantifier():
            return False
        return True

    def __ne__(self, other):
        return not(self.__eq__(other))


if __name__ == '__main__':
    c1 = Clause()
    c1.set_word("word")
    c2 = Clause()
    print(c1 != c2)