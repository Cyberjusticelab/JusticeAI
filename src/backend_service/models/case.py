# coding=iso-8859-1

import re
import codecs


class Case:
    def __init__(self, file_path):
        self.no_dossier = 0
        self.no_demande = 0
        self.no_demande_rectified = 0
        self.date = 0
        self.is_tenant = False
        self.is_rectified = False
        self.total_hearings = 0
        self.open_file(file_path=file_path)

    def open_file(self, file_path):
        file = codecs.open(file_path, 'r', 'iso-8859-1')
        for line in file:
            if self.no_dossier == 0 and re.search("No dossier", line):
                next_line = file.next()
                if re.search("^[0-9]", next_line) is not None:
                    self.no_dossier = next_line
                    continue
            if self.no_demande == 0 and re.search("No demande", line):
                next_line = file.next()
                if re.search("^[0-9]", next_line) is not None:
                    self.no_demande = next_line
                    continue
            if re.search("D\s*É\s*C\s*I\s*S\s*I\s*O\s*N\s*R\s*E\s*C\s*T\s*I\s*F\s*I\s*É\s*E", line):
                self.is_rectified = True
            if re.search("^Date\s*:", line):
                self.total_hearings += 1

import os

count = 0
for fname in os.listdir('/Users/taimoorrana/Downloads/text_bk/'):
    case = Case('/Users/taimoorrana/Downloads/text_bk/' + fname)
    if count > 100:
        break
    count += 1
    print fname, ": ", case.total_hearings
