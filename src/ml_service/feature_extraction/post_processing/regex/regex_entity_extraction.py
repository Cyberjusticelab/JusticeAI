from util.file import Load
import re


class EntityExtraction:
    __regex_bin = None
    one_day = 86400 # unix time for 1 day

    def __init__(self):
        pass
    
    @staticmethod
    def match_any_regex(text, regex_array, regex_type):
        """
            Returns True if any of the regex in regex_array
            are found in the given text string
        """
        if EntityExtraction.__regex_bin is None:
            EntityExtraction.__regex_bin = Load.load_binary('regexes.bin')

        for regex in regex_array:
            if regex.search(text): 
                return EntityExtraction.__extract_regex_entity(text, regex_type)
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

        if regex_type == 'BOOLEAN':
            return True, 1

        elif regex_type == 'MONEY_REGEX':
            generic_regex = re.compile(EntityExtraction.__regex_bin[regex_type])
            entity = generic_regex.search(text).group(0)

            # Functional but not sure about how optimal it is
            entity = entity.replace("$", "")
            entity = entity.replace(" ", "")
            entity = entity.replace(",", ".")
            return True, entity
    
    @staticmethod
    def __time_to_unix(time):
        pass
