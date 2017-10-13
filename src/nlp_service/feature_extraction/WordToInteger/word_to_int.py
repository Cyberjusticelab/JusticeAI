'''
Code inspired by stackoverflow :)
'''


class WordToInt():
    units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
    ]

    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    scales = ["hundred", "thousand", "million", "billion", "trillion"]

    #####################################################
    # CONSTRUCTOR
    def __init__(self):
        self.__num_words = {}
        self.__init_dictionary()

    #####################################################
    # INIT DICTIONARY
    def __init_dictionary(self):
        self.__num_words["and"] = (1, 0)
        for idx, word in enumerate(self.units):
            self.__num_words[word] = (1, idx)
        for idx, word in enumerate(self.tens):
            self.__num_words[word] = (1, idx * 10)
        for idx, word in enumerate(self.scales):
            self.__num_words[word] = (10 ** (idx * 3 or 2), 0)

    #####################################################
    # TEXT TO INT
    # ---------------------------------------------------
    # Converts a string to an number
    # nine hundred --> 900
    #
    # text: string
    # returns: int
    def text2int(self, text):
        current = result = 0
        for word in text.split():
            if word not in self.__num_words:
                raise Exception("Illegal word: " + word)

            scale, increment = self.__num_words[word]
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0

        return result + current


if __name__ == '__main__':
    converter = WordToInt()
    result = converter.text2int("eight hundred two")
    print(result)
