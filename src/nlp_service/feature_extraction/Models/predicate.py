from feature_extraction.GlobalVariables import regex

from feature_extraction.Models import Abstract_Model

'''
PREDICATE
----------------------------------------------
Verb / link word with adverbs
'''


class Predicate(Abstract_Model.AbstractModel):
    def __init__(self):
        Abstract_Model.AbstractModel.__init__(self)

    ##########################################
    # ADD WORD
    # ----------------------------------------
    # word: String
    # tag: String
    def add_word(self, word, tag):
        if not (regex.Regex.verb_match.match(tag)):
            return
        self._word.append((word, tag))
        self.add_tag_index(tag)

    ##########################################
    # MERGE
    # ----------------------------------------
    # Merges 2 predicates as one
    # other: Predicate object
    def merge(self, other):
        if len(self.get_word()) == 0:
            for word in other.get_word():
                self.add_word(word[0], word[1])
        elif len(other.get_word()) == 0:
            pass
        else:
            for word in other.get_word():
                self.add_word(word[0], word[1])
        self._attribute.extend(other.get_attribute())

    def empty_model(self):
        if len(self.get_word()) > 0:
            return False
        elif len(self.get_attribute()) > 0:
            return False
        return True

    def __str__(self):
        return "PREDICATE: " + str(self._word) + \
               " | Qualifier: " + str(self._attribute)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        elif not (self.equal_lists(self.get_attribute(), other.get_attribute())):
            return False
        elif self.get_word() != other.get_word():
            return False
        return True

    def __ne__(self, other):
        return not (self.__eq__(other))
