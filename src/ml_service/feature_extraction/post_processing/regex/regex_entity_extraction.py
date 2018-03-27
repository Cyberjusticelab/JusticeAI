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
        'fevrier': 2,
        'mars': 3,
        'avril': 4,
        'mai': 5,
        'juin': 6,
        'juillet': 7,
        'aout': 8,
        'septembre': 9,
        "octobre": 10,
        'novembre': 11,
        'decembre': 12
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
            return EntityExtraction.__regex_money(regex_type, sentence)

        elif regex_type == 'DATE_REGEX':
            return EntityExtraction.__regex_date('DURATION_REGEX', sentence)
        return False, 0

    @staticmethod
    def __regex_date(regex_type, sentence):
        """

        1) create the date regex --> re.compile(regex string)
        2) find all date entities in the sentence --> returns a list
        3) get all the integer values associated to dates
        4) sort the dates in ascending order
        5) start date is the first element of the list
        6) end date is the last element
        7) convert to unix. ** We don't care about the year
            7.1) start date we assume is the first day of a month
            7.2) end date we assume the last day of the month. 28 is chosen because
                 every month have at least 28 days
            7.3) some dates have a "d'" such as d'octobre... so we replace d' with ''
        8)get the time difference from unix to days

        :param regex_type: str(DATE_REGEX)
        :param sentence: sentence to extract entities
        :return: boolean, integer
        """

        start_end_date_regex = re.compile(r"(?i)(\d{1,2})?(?:er|èr|ere|em|eme|ème)?\s?(\w{3,9}) (\d{4}) (?:a|à|au|et|et se terminant le) (\d{1,2})?(?:er|èr|ere|em|eme|ème)?\s?(\w{3,9}) (\d{4})",re.IGNORECASE)
        entities = re.findall(start_end_date_regex, sentence)

        if entities.__len__() > 0:
            entities = re.findall(start_end_date_regex, sentence).pop(0)

            try:
                start_day = int(entities[0])
            except ValueError as error:
                Log.write(str(error) + ": could not convert " + entities[0] + " to an int")
                start_day = '1'

            start_month = ''
            try:
                start_month = str(EntityExtraction.month_dict[entities[1]])
            except IndexError as error:
                Log.write(str(error) + ":" + str(start_month) + " is not a month or has spelling mistake")
                return False, 0

            start_year = entities[2]

            try:
                end_day = int(entities[3])
            except ValueError as error:
                Log.write(str(error) + ": could not convert " + entities[3] + " to an int")
                end_day = '28'

            try:
                end_month = str(EntityExtraction.month_dict[entities[4]])
            except IndexError as error:
                Log.write(str(error) + ":" + str(start_month) + " is not a month or has spelling mistake")
                return False, 0

            end_year = entities[5]

            start_unix = EntityExtraction.__date_to_unix([start_day, start_month, start_year])
            end_unix = EntityExtraction.__date_to_unix([end_day, end_month, end_year])

            return True, EntityExtraction.__get_time_interval_in_days(start_unix, end_unix)

        months_enumaration_regex = re.compile(
            r"(janvier|février|mars|avril|d'avril|mai|juin|juillet|d'août|août|aout|septembre|d'octobre|octobre|novembre|décembre|decembre)",
            re.IGNORECASE)

        entities = re.findall(months_enumaration_regex, sentence)
        if entities.__len__() > 1:
            total_months = entities.__len__()
            start_unix = EntityExtraction.__date_to_unix(['1', '1', '1970'])
            end_unix = EntityExtraction.__date_to_unix(['28', str(total_months), '1970'])
            return True, EntityExtraction.__get_time_interval_in_days(start_unix, end_unix)

        return False, 0

    @staticmethod
    def __regex_money(regex_type, sentence):
        """

        1) create the date regex --> re.compile(regex string)
        2) Find the dollar amount in the sentence
        3) filter the string by removing unecessary characters
        4) return the entity

        :param regex_type: str(MONEY_REGEX)
        :param sentence: boolean, integer
        :return:
        """
        generic_regex = re.compile(EntityExtraction.regex_bin[regex_type])
        entity = generic_regex.search(sentence).group(0)

        # Functional but not sure about how optimal it is
        entity = entity.replace("$", "")
        entity = entity.replace(" ", "")
        entity = entity.replace(",", ".")
        if entity[-1] == '.':
            entity = entity[:-1]
        return True, entity

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
