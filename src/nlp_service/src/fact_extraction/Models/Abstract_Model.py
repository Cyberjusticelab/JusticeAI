'''
ABSTRACT MODEL
-----------------------------------------
'''


class AbstractModel:
    def __init__(self):
        self.__word = None
        self.__qualifier = []

    def set_word(self, word):
        if self.__word is None:
            self.__word = word
        else:
            self.__word += ", " + word

    def set_quantifier(self, quantifier):
        self.__quantifier = quantifier

    def add_qualifier(self, qualifier):
        self.__qualifier.append(qualifier)

