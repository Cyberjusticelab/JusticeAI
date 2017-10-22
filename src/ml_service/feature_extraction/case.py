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

        for line in current_file:

            # Extract "No dossier" ID
            if self.no_dossier == 0 and re.search("^[N|n]o[s]? dossier[s]?\s*:", line):
                next_line = current_file.next()

                # if the next line contains numbers then it's the ID we are looking for
                if re.search("^[0-9]", next_line) is not None:
                    self.no_dossier = next_line
                    self.data["noDossier"] = next_line.replace("\r", "")
                    continue

            # Extract "No demande" ID
            if self.no_demande == 0 and re.search("^[N|n]o[s]? demande[s]?\s*:", line):
                next_line = current_file.next()

                # if the next line contains numbers then it's the ID we are looking for
                if re.search("^[0-9]", next_line) is not None:
                    self.no_demande = next_line
                    self.data["noDemande"] = next_line.replace("\r", "")
                    continue
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

        self.data["totalHearings"] = self.total_hearings


def writeToJSONFile(path, file_name, data):
    with open(path + '/' + file_name + ".json","w+") as JSON_File:
        json.dump(data, JSON_File)


# Path of the cases directory
directory_path = "/Users/taimoorrana/Downloads/text_bk/"
for file_name in os.listdir(directory_path):
    if file_name != ".DS_Store":
        case = Case(directory_path + file_name)
        writeToJSONFile('/Users/taimoorrana/Desktop/testJson', "case#"+case.no_demande, case.data)
        print file_name, ": ", case.total_hearings
