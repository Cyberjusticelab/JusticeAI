# coding=iso-8859-1

import re
import codecs
import json
import os


class Case:
    def __init__(self, file_path):
        self.data = {"fileID": 0, "applicationID": 0, "isRectified": False, "totalHearings": 0}
        self._open_file(file_path=file_path)

    def _open_file(self, file_path):
        current_file = codecs.open(file_path, 'r', "iso-8859-1")

        for line in current_file:

            # Extract "No dossier" ID
            if self.data["fileID"] == 0 and re.search("^[N|n]o[s]? dossier[s]?\s*:", line):
                line = current_file.readline().strip()

                while line == "":
                    line = current_file.readline().strip()

                file_ids = []
                # If the next line contains numbers then it's the ID we are looking for
                while re.search("^\d{2}.+[A-Z]$", line) is not None:
                    file_ids.append(line)
                    line = current_file.readline().strip()

                self.data["fileID"] = file_ids

            # Extract "No demande" ID
            if self.data["applicationID"] == 0 and re.search("^[N|n]o[s]? demande[s]?\s*:", line):
                line = current_file.readline().strip()

                while line == "":
                    line = current_file.readline().strip()

                application_ids = []
                # If the next line contains numbers then it's the ID we are looking for
                while re.search("^\d.*\d$", line) is not None:
                    for id in line.split(" et "):
                        application_ids.append(id)
                    line = current_file.readline().strip()

                self.data["applicationID"] = application_ids

            '''
            Extract total amount of hearings.
            Each hearing has a date stamp.
            Counting each date stamp give us the total amount of hearing for this case.
            '''
            if re.search("^[D|d]ate\s*:", line):
                self.data["totalHearings"] += 1

        # If total hearing is greater than 1, then the case was rectified
        if self.data["totalHearings"] > 1:
            self.data["isRectified"] = True


# Writes old_data to a given file
def write_to_json_file(path, file_name, data):
    with open(path + '/' + file_name + ".json", "w+") as json_file:
        json.dump(data, json_file)


# Reads all cases from a given directory and outputs relevant old_data in the given output directory
def extract_data_from_cases(cases_directory, output_directory):
    for file_name in os.listdir(cases_directory):
        case = Case(cases_directory + file_name)
        write_to_json_file(output_directory, "case#" + case.data["applicationID"][0], case.data)
