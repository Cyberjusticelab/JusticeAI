import codecs
import os
import re

claim_text = []


def _extract_facts(file_path):
    # Read file
    current_file = codecs.open(file_path, 'r', "iso-8859-1")

    # Determine how many claims/facts exists
    claim_count = 0
    date_count = 0

    for line in current_file:

        # if the case is in english, fact are not extracted
        if re.search("the|rent|time|landlord|payment|amount", line):
            return

        # each hearing starts with a date
        # extrating fact from the first hearing only
        if re.search("^[D|d]ate\s*:", line):
            date_count += 1
            if date_count > 1:
                break

        if re.search("\[\d+\]", line):
            claim_count += 1

        if re.search('POUR CES MOTIFS, LE TRIBUNAL', line):  # this defines the end of facts
            break

    # reset file reader head
    current_file.seek(0)

    line = current_file.readline().strip()
    get_next_line = True

    # extract and save those claims
    while claim_count > 0:
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
            break
        _extract_facts(cases_directory + file_name)
        count += 1
    return claim_text
