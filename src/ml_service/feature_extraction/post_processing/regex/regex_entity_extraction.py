from feature_extraction.post_processing.regex.regex_lib import RegexLib
import re
import datetime
import time
import unicodedata
from util.log import Log


class EntityExtraction:
    regex_bin = None
    one_day = 86400  # unix time for 1 day
    month_dict = {
        'janvier': 1,
        'février': 2,
        'mars': 3,
        'avril': 4,
        'mai': 5,
        'juin': 6,
        'juillet': 7,
        'août': 8,
        'septembre': 9,
        "octobre": 10,
        'novembre': 11,
        'décembre': 12
    }

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
        if EntityExtraction.regex_bin is None:
            EntityExtraction.regex_bin = RegexLib.model
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

        # removes accents
        nfkd_form = unicodedata.normalize('NFKD', sentence)
        sentence = u"".join([character for character in nfkd_form if not unicodedata.combining(character)])

        if regex_type == 'BOOLEAN':
            return True, 1

        elif regex_type == 'MONEY_REGEX':
            generic_regex = re.compile(EntityExtraction.regex_bin[regex_type])
            entity = generic_regex.search(sentence).group(0)

            # Functional but not sure about how optimal it is
            entity = entity.replace("$", "")
            entity = entity.replace(" ", "")
            entity = entity.replace(",", ".")
            if entity[-1] == '.':
                entity = entity[:-1]
            return True, entity

        elif regex_type == 'DATE_REGEX':
            generic_regex = re.compile(EntityExtraction.regex_bin[regex_type])
            entities = generic_regex.findall(sentence)
            try:
                start = EntityExtraction.month_dict[entities[0].replace("d'", '')]
                end = EntityExtraction.month_dict[entities[len(entities) - 1].replace("d'", '')]
                start_unix = EntityExtraction.__date_to_unix(['1', str(start), '1970'])
                end_unix = EntityExtraction.__date_to_unix(['28', str(end), '1970'])
                return True, EntityExtraction.__get_time_interval_in_days(start_unix, end_unix)
            except KeyError:
                Log.write("spelling error: " + str(entities))
        return False, 0

    @staticmethod
    def __date_to_unix(date):
        """
        Given a date list (ex: [30,12,2019]) this function gets the unix time that represents this date
        :param date: date to convert into unix time
        :return: unix time representing the input date
        """
        date_string = " ".join(date)
        try:
            unix_time = time.mktime(datetime.datetime.strptime(date_string, '%d %m %Y').timetuple())
        except (ValueError, OverflowError) as error:
            Log.write(str(error) + ": " + str(date_string))
            return None

        return unix_time

    @staticmethod
    def __get_time_interval_in_days(first_date, second_date):
        """
        Calculates the time difference between 2 dates
        :param first_date: date in unix time
        :param second_date: date in unix time
        :return: time difference between 2 dates
        """
        return int(abs(first_date - second_date) / EntityExtraction.one_day)
