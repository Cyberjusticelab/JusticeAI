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

    def __str__(self):
        return "CLAUSE: " + str(self._word) + \
               " | Qualifier: " + str(self._qualifier) + \
               " | Quantifier: " + str(self.__quantifier)

