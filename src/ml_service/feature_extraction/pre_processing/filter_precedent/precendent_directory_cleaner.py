import os
import regex as re
from langdetect import detect
from util.constant import Path
from sys import stdout
from util.log import Log

FACT_DIGIT_REGEX = r"\[\d+\]"
TENANT_REGEX = r"locataire(s)?"
LANDLORD_REGEX = r"locat(eur|rice)(s)?"


def __multiple_words(min, max):
    return r"(\w+(\s|'|,\s)){" + str(min) + "," + str(max) + "}"


regexes = [
    # absent
    re.compile(
        FACT_DIGIT_REGEX +
        r".+considérant l'absence (du|de la|des) (" +
        LANDLORD_REGEX + r"|" + TENANT_REGEX + r")",
        re.IGNORECASE
    ),
    # incorrect_facts
    re.compile(
        FACT_DIGIT_REGEX + \
        r".+demande (de la|des) " + TENANT_REGEX + r" est mal fondée",
        re.IGNORECASE
    ),
    # tenant_landlord_agreement
    re.compile(
        FACT_DIGIT_REGEX + r".+entente.+(entre\sles\sdeux\sparties)",
        re.IGNORECASE
    ),
    re.compile(
        FACT_DIGIT_REGEX + r".+entérine (l'|cette\s)entente",
        re.IGNORECASE
    ),
    re.compile(
        FACT_DIGIT_REGEX + r".+l'entente intervenue entre les parties",
        re.IGNORECASE
    ),
    re.compile(
        FACT_DIGIT_REGEX + r".+homologue cette entente",
        re.IGNORECASE
    ),
    re.compile(
        FACT_DIGIT_REGEX + r".+homologue " + \
        __multiple_words(0, 3) + r"transaction",
        re.IGNORECASE
    ),
    # tenant_rent_paid_before_hearing
    re.compile(
        FACT_DIGIT_REGEX + r".+" + TENANT_REGEX + \
        r".*payé.*loyer.*(dû le jour|avant).+(audience)",
        re.IGNORECASE
    ),
    re.compile(
        FACT_DIGIT_REGEX + \
        r".+(ont|a|ayant) payé (le|tous les) loyer(s|) (dû|du)",
        re.IGNORECASE
    ),
    re.compile(
        FACT_DIGIT_REGEX + r".+(ont|a) payé les loyers réclamés",
        re.IGNORECASE
    ),
    re.compile(
        FACT_DIGIT_REGEX + r".+les loyers ont été payés",
        re.IGNORECASE
    ),
    re.compile(
        FACT_DIGIT_REGEX + r".+à la date de l'audience, tous les loyers réclamés ont été payés",
        re.IGNORECASE
    )
]


def remove_files(directory_path):
    """
    removes precedents that matches the regex list or are written in english
    :param directory_path: directory where the precedents are located
    :return: (names of files removed due to regex match, names of files that were in english)
    """
    files_matching_regexes = []
    files_in_english = []
    files_parse = 0
    nb_of_files = len(os.listdir(directory_path))
    Log.write('Filtering precedents')
    for filename in os.listdir(directory_path):
        percent = float(files_parse / nb_of_files) * 100
        stdout.write("\rINFO: Filtering: %f " % percent + "%")
        stdout.flush()
        files_parse += 1

        if filename.endswith(".txt"):
            precedent_file = open(directory_path + filename, "r", encoding="ISO-8859-1")
            file_removed = False

            # remove precedents that matches regexes
            for line in precedent_file.readlines():
                for reg in regexes:
                    if reg.search(line):
                        os.remove(directory_path + filename)
                        file_removed = True
                        files_matching_regexes.append(filename)
                        break
                if file_removed:
                    break
            if file_removed:
                precedent_file.close()
                continue

            # remove english precedents
            precedent_file.seek(0)
            file_content = precedent_file.read()
            if detect(file_content) == 'en':
                os.remove(directory_path + filename)
                files_in_english.append(filename)
            precedent_file.close()
    print('')
    Log.write('Done filtering precedents')
    Log.write('Removed {} file in english'.format(str(len(files_in_english))))
    Log.write('Removed {} files without value'.format(str(len(files_matching_regexes))))
    return files_in_english, files_matching_regexes


def run(command):
    remove_files(Path.raw_data_directory)
