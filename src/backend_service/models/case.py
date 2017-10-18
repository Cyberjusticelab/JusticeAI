import re
import codecs


class Case:
    def __init__(self, file_path):
        self.no_dossier = 0
        self.no_demande = 0
        self.date = 0
        self.is_tenant = False
        self.is_rectified = False
        self.total_hearings = 0
        self.open_file(file_path=file_path)

    def open_file(self, file_path):
        file = codecs.open(file_path, 'r', 'iso-8859-1')
        for line in file:
            print line
            search_obj = re.search("No dossier:", line)
            if search_obj and self.no_dossier == 0:
                self.no_dossier = file.next()
                continue
            search_obj = re.search("No demande:", line)
            if search_obj and self.no_demande == 0:
                self.no_demande = file.next()
                continue
            search_obj = re.search("Date :", line)
            if search_obj:
                self.date = file.next()
                continue
            search_obj = re.search("R E C T I F I", line)
            if search_obj:
                self.is_rectified = True
            if re.search("C I S I O N", line):
                self.total_hearings += 1

case = Case("test.txt")
print case.date
print case.no_dossier
print case.no_demande
print case.total_hearings
print case.is_rectified