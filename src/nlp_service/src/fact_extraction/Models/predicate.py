from src.fact_extraction.Models import Abstract_Model
from src.fact_extraction.GlobalVariables import regex


'''
PREDICATE
----------------------------------------------
Verb / link word with adverbs
'''


class Predicate(Abstract_Model.AbstractModel):
    def __init__(self):
        Abstract_Model.AbstractModel.__init__(self)

    def __str__(self):
        return "PREDICATE: " + str(self._word) + \
               " | Qualifier: " + str(self._qualifier)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        elif not(self.equal_lists(self.get_qualifier(), other.get_qualifier())):
            return False
        elif self.get_word() != other.get_word():
            return False
        return True

    def __ne__(self, other):
        return not(self.__eq__(other))

    def set_word(self, word, tag = None):
        if tag is not None:
            if not(regex.Regex.verb_match.match(tag)):
                return
        if self._word is None:
            self._word = word
        else:
            self._word += ", " + word

    def merge(self, other):
        if self.get_word() is None:
            self.set_word(other.get_word())
        elif other.get_word() is None:
            pass
        else:
            self.set_word(other.get_word())
        self._qualifier.extend(other.get_qualifier())

if __name__ == '__main__':
    p1 = Predicate()
    p1.add_qualifier("word")
    p2 = Predicate()
    p2.add_qualifier("word")
    print(p1 == p2)