'''
ABSTRACT MODEL
-----------------------------------------
'''


class AbstractModel:
    def __init__(self):
        self._word = None
        self._qualifier = []

    def set_word(self, word):
        if self._word is None:
            self._word = word
        else:
            self._word += ", " + word

    def get_word(self):
        return self._word

    def get_qualifier(self):
        return self._qualifier.copy()

    def add_qualifier(self, qualifier):
        self._qualifier.append(qualifier)

