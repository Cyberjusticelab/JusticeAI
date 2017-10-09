class Predicate:
    def __init__(self):
        self.__word = None
        self.__qualifier = []

    def set_word(self, word):
        if self.__word is None:
            self.__word = word
        else:
            self.__word += ", " + word

    def get_word(self):
        return self.__word

    def add_qualifier(self, qualifier):
        self.__qualifier.append(qualifier)

    def __str__(self):
        return "PREDICATE: " + str(self.__word) + \
               " | Qualifier: " + str(self.__qualifier)