from util.file import Load


class RegexLogic:
    __regex_bin = Load.load_binary('regexes.bin')
    
    def __init__(self):
        pass
    
    @staticmethod
    def match_any_regex(text, regex_array, regex_type):
        """
            Returns True if any of the regex in regex_array
            are found in the given text string
        """
        for regex in regex_array:
            if regex.search(text): 
                return RegexLogic.__extract_regex_entity(text, regex_type)
        return False, 0
    
    @staticmethod
    def __extract_regex_entity(text, regex_type):
        """
        Extract integer value from the text
        :param text: string to regex
        :param regex: regex logic
        :param regex_type: type of information to extract
        :return: (boolean, int)
        """
        if regex_type is 'bool':
            return (True, 1)
        else:
            return True, RegexLogic.__regex_bin[regex_type].match(text)[0]
    
    @staticmethod
    def __time_to_unix(time):
        pass

