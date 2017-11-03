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
    for line in current_file:
        if re.search("^[D|d]ate\s*:", line):
            date_count += 1
            if date_count > 1:
                break
        if re.search("\[\d+\]", line):
            claim_count += 1
        if re.search('POUR CES MOTIFS, LE TRIBUNAL', line):
            break
    current_file.seek(0)
    line = current_file.readline().strip()
    get_next_line = True

    # extract and save those claims
    while claim_count > 0:
        if re.search("\[\d+\]", line):
            claim_count -= 1
            line = re.sub("[\d*\s*]*\d+[,]?\d*\s*\$", " frais ", line)
            claim = line[4:]  # this gets rid of the [12] tags in front of each fact
            line = current_file.readline().strip()
            get_next_line = False

            while re.search("\[\d+\]", line) is None and line != '':
                line = current_file.readline().strip()
                line = re.sub("[\d*\s*]*\d+[,]?\d*\s*\$", " frais ", line)
                if re.search('POUR CES MOTIFS, LE TRIBUNAL', line):
                    line = line.replace('POUR CES MOTIFS, LE TRIBUNAL', "")
                    claim += line
                    claim_text.append(claim)
                    break
                claim += line
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
            break
        _open_file(cases_directory + file_name)
        count += 1
    return claim_text


