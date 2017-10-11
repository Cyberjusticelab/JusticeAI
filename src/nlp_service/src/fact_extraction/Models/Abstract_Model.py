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
        if qualifier is not None:
            self._qualifier.append(qualifier)

    @staticmethod
    def equal_lists(list1, list2):
        if len(list1) != len(list2):
            return False

        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return False
        return True

