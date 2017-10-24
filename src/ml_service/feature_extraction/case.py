# coding=iso-8859-1

import re
import codecs
import os
import json


class Case:
    def __init__(self, file_path):
        self.data = {"noDossier": 0, "noDemande": 0, "isRectified": False, "totalHearings": 0}
        self._open_file(file_path=file_path)

    def _open_file(self, file_path):
        current_file = codecs.open(file_path, 'r', "iso-8859-1")

        for line in current_file:

            # Extract "No dossier" ID
            if self.data["noDossier"] == 0 and re.search("^[N|n]o[s]? dossier[s]?\s*:", line):
                line = current_file.next().strip()

                while line == "":
                    line = current_file.next().strip()

                data = []
                # If the next line contains numbers then it's the ID we are looking for
                while re.search("^\d{2}.+[A-Z]$", line) is not None:
                    data.append(line)
                    line = current_file.next().strip()

                self.data["noDossier"] = data

            # Extract "No demande" ID
            if self.data["noDemande"] == 0 and re.search("^[N|n]o[s]? demande[s]?\s*:", line):
                line = current_file.next().strip()

                while line == "":
                    line = current_file.next().strip()

                data = []
                # If the next line contains numbers then it's the ID we are looking for
                while re.search("^\d.*\d$", line) is not None:
                    for id in line.split(" et "):
                        data.append(id)
                    line = current_file.next().strip()

                self.data["noDemande"] = data

            # Extract total amount of hearings
            # Each hearing has a date stamp. Counting each date stamp give us the total amount of hearing for this case
            if re.search("^[D|d]ate\s*:", line):
                self.data["totalHearings"] += 1

        # If total hearing is greater than 1, then the case was rectified
        if self.data["totalHearings"] > 1:
            self.data["isRectified"] = True


def write_to_json_file(path, file_name, data):
    with open(path + '/' + file_name + ".json", "w+") as JSON_File:
        json.dump(data, JSON_File)


# Path of the cases directory
directory_path = "./dummy_cases/"
for file_name in os.listdir(directory_path):
    case = Case(directory_path + file_name)
    write_to_json_file('./case_info_extracted', "case#" + case.data["noDemande"][0], case.data)
    print file_name, ": ", case.data["noDossier"], case.data["noDemande"]
