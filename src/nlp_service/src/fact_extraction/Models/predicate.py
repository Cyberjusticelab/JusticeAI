from src.fact_extraction.Models import Abstract_Model


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
        elif set(self.get_qualifier()) != set(other.get_qualifier):
            return False
        elif self.get_word() != other.get_word():
            return False
        return True
