from src.fact_extraction.Models import Abstract_Model


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
        self.__quantifier = quantifier

    def get_quantifier(self):
        return self.__quantifier

    def __str__(self):
        return "CLAUSE: " + str(self._word) + \
               " | Qualifier: " + str(self._qualifier) + \
               " | Quantifier: " + str(self.__quantifier)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        elif set(self.get_qualifier()) != set(other.get_qualifier):
            return False
        elif self.get_word() != other.get_word():
            return False
        elif self.get_quantifier() != other.get_quantifier:
            return False
        return True
