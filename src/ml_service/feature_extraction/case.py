# coding=iso-8859-1

import re
import codecs
import os
import json


class Case:
    def __init__(self, file_path):
        self.no_dossier = 0
        self.no_demande = 0
        self.is_rectified = False
        self.total_hearings = 0
        self.data = {}
        self._open_file(file_path=file_path)

    def _open_file(self, file_path):
        current_file = codecs.open(file_path, 'r', "iso-8859-1")

        if file_name == "AZ-51145180.txt":
            test = "gsdgs"
        for line in current_file:

            # Extract "No dossier" ID
            if self.no_dossier == 0 and re.search("^[N|n]o[s]? dossier[s]?\s*:", line):
                line = current_file.next().strip()

                while line == "":
                    line = current_file.next().strip()

                count = 0
                data = []
                # if the next line contains numbers then it's the ID we are looking for
                while re.search("^[0-9]{2}.+[A-Z]$", line) is not None:
                    self.no_dossier = line.strip()
                    data.append(line.strip())
                    line = current_file.next().strip()
                    count += 1

                if count > 1:
                    print file_name
                self.data["noDossier"] = data

            # Extract "No demande" ID
            if self.no_demande == 0 and re.search("^[N|n]o[s]? demande[s]?\s*:", line):
                line = current_file.next().strip()

                while line == "":
                    line = current_file.next().strip()
                # if the next line contains numbers then it's the ID we are looking for
                data = []
                count = 0

                while re.search("^[0-9].*[0-9]$", line) is not None:
                    self.no_demande = line.strip()
                    for id in line.strip().split(" et "):
                        data.append(id)
                    line = current_file.next().strip()
                    count += 1

                self.data["noDemande"] = data

            # Extract total amount of hearings
            # Each hearing has a date stamp. Counting each date stamp give us the total amount of hearing for this case
            if re.search("^[D|d]ate\s*:", line):
                self.total_hearings += 1

        # If no hearings were found, something went wrong
        if self.total_hearings == 0:
            print "Unable to find a hearing in ", file_path

        # If total hearing is greater than 1, then the case was rectified
        if self.total_hearings > 1:
            self.is_rectified = True
            self.data["isRectified"] = True
        else:
            self.data["isRectified"] = False
        self.data["totalHearings"] = self.total_hearings


def writeToJSONFile(path, file_name, data):
    with open(path + '/' + file_name + ".json", "w+") as JSON_File:
        json.dump(data, JSON_File)


# Path of the cases directory
directory_path = "/Users/taimoorrana/Downloads/text_bk/"
for file_name in os.listdir(directory_path):
    if file_name != ".DS_Store":
        case = Case(directory_path + file_name)
        writeToJSONFile('/Users/taimoorrana/Desktop/testJson', "case#" + case.no_demande, case.data)
        print file_name, ": ", case.data["noDossier"], case.data["noDemande"]
