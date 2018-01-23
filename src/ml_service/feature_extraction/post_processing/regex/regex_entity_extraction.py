from util.file import Load
import re
import enchant
import datetime
import time


class EntityExtraction:
    __regex_bin = None
    one_day = 86400 # unix time for 1 day
    month_dict = {'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6,
                  'juillet': 7, 'août': 8, 'septembre': 9, "octobre": 10, 'novembre': 11, 'décembre': 12}

    @staticmethod
    def month_name_corrector(month_name_with_mistake):
        dictionary = enchant.Dict('fr_FR')
        possible_words = dictionary.suggest(month_name_with_mistake)
        for word in possible_words:
            if word in EntityExtraction.month_dict:
                return word

    def __init__(self):
        pass
    
    @staticmethod
    def match_any_regex(text, regex_array, regex_type):
        """
        1) Loads the regex binaries only once. If it is loaded then continue.
        2) Iterate all the regex and search text
        3) if regex finds a match then extract entity from this sub sentence

        :param text: String representation of precedent
        :param regex_array: List of regex
        :param regex_type: Entity we look for in a particular regex match
        :return: (Boolean, entity<int>)
        """
        if EntityExtraction.__regex_bin is None:
            EntityExtraction.__regex_bin = Load.load_binary('regexes.bin')
        for regex in regex_array:
            regex_result = regex.search(text)
            if regex_result:
                sentence = regex_result.group(0).lower()
                return EntityExtraction.__extract_regex_entity(sentence, regex_type)
        return False, 0
    
    @staticmethod
    def __extract_regex_entity(sentence, regex_type):
        """
        Entity extraction from the text

        1) If the type is BOOLEAN then simply return True, 1
        2) If the type is MONEY_REGEX then extract the money value and format string so that it is
           convertible to integer
        3) else return False, 1

        :param sentence: sub sentence from text to apply regex
        :param regex_type: type of information to extract
        :return: (boolean, int)
        """

        if regex_type == 'BOOLEAN':
            return True, 1

        elif regex_type == 'MONEY_REGEX':
            generic_regex = re.compile(EntityExtraction.__regex_bin[regex_type])
            entity = generic_regex.search(sentence).group(0)

            # Functional but not sure about how optimal it is
            entity = entity.replace("$", "")
            entity = entity.replace(" ", "")
            entity = entity.replace(",", ".")
            if entity[-1] == '.':
                entity = entity[:-1]
            return True, entity

        elif regex_type == 'DATE_REGEX':
            date_components = sentence.split(" ")

            """
            the value 3 is used to make sure we have all the required components. 
            1 for the day, 1 for the month and 1 for the year.
            """
            if len(date_components) == 3:
                date_components[0] = re.sub(r"er|ere|em|eme", "", date_components[0])
                try:
                    date_components[1] = str(EntityExtraction.month_dict[date_components[1]])
                except KeyError:
                    date_components[1] = str(EntityExtraction.month_dict[EntityExtraction.month_name_corrector(date_components[1])])
                date_components[2] = date_components[2]
                return True, EntityExtraction.__date_to_unix(date_components)

        return False, 0
    
    @staticmethod
    def __date_to_unix(date):
        """
        Given a date list (ex: [30,12,2019]) this function gets the unix time the represents this date
        :param date: date to convert into unix time
        :return: unix time representing the input date
        """
        date_string = " ".join(date)
        unix_time = time.mktime(datetime.datetime.strptime(date_string, '%d %m %Y').timetuple())
        return unix_time

    @staticmethod
    def __get_time_interval_in_days(first_date, second_date):
        """
        Calculates the time difference between 2 dates
        :param first_date: date in unix time
        :param second_date: date in unix time
        :return: time difference between 2 dates
        """
        return abs(first_date - second_date) / EntityExtraction.one_day