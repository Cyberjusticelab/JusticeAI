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

    def set_word(self, word, tag):
        if not(regex.Regex.verb_match.match(tag)):
            return
        self._word.append((word, tag))
        self.add_tag_index(tag)

    def merge(self, other):
        if len(self.get_word()) == 0:
            for word in other.get_word():
                self.set_word(word[0], word[1])
        elif len(other.get_word()) == 0:
            pass
        else:
            for word in other.get_word():
                self.set_word(word[0], word[1])
        self._qualifier.extend(other.get_qualifier())

    def empty_model(self):
        if len(self.get_word()) > 0:
            return False
        elif len(self.get_qualifier()) > 0:
            return False
        return True

if __name__ == '__main__':
    p1 = Predicate()
    p1.add_qualifier("word", 'VBN')
    p2 = Predicate()
    p2.add_qualifier("word", 'VBN')
    print(p1 == p2)