import codecs
import os
import re
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("french")

claim_text = []


def _open_file(file_path):
    # Read file
    current_file = codecs.open(file_path, 'r', "iso-8859-1")

    # how many claims are there?
    claim_count = 0
    date_count = 0
    is_english = False
    for line in current_file:
        if re.search("^[D|d]ate\s*:", line):
            date_count += 1
            if date_count > 1:
                break
        if re.search("the|rent|time|landlord|payment|amount", line):
            is_english = True
            break
        if re.search("\[\d+\]", line):
            claim_count += 1
        if re.search('POUR CES MOTIFS, LE TRIBUNAL', line):
            break
    current_file.seek(0)
    line = current_file.readline().strip()
    get_next_line = True

    # extract and save those claims
    while claim_count > 0 and not is_english:
        if re.search("\[\d+\]", line):
            claim_count -= 1
            claim = line
            line = current_file.readline().strip()
            get_next_line = False

            while re.search("\[\d+\]", line) is None and line != '':
                claim += line
                line = current_file.readline().strip()
            claim_text.append(claim)
            if line == '':
                break
        if get_next_line:
            line = current_file.readline().strip()


# Reads all cases from a given directory and outputs relevant data in the given output directory
def extract_data_from_cases(cases_directory, total_files_to_process):
    count = 0
    for file_name in os.listdir(cases_directory):
        if count == total_files_to_process:
            print(file_name)
            print("finished Extraction")
            break
        _open_file(cases_directory + file_name)
        count += 1
        if count % 100 == 0:
            print(count)
    return claim_text


