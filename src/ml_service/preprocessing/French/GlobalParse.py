from src.ml_service.preprocessing.French.DecisionParse import Precedence_Parser
from src.ml_service.preprocessing.French.Model import PrecedenceModel


class Global_Parser(Precedence_Parser):
    def __init__(self, file_directory):
        Precedence_Parser.__init__(self)
        self.file_directory = file_directory

    def parse(self, filename):
        self.__model = PrecedenceModel()
        self.__extract(filename)
        self.__model.format()
        return self.__model

    def __extract(self, filename):
        file = open(self.file_directory + filename, 'r', encoding="ISO-8859-1")
        for line in file:
            sub_sent = self.__split_sub_sentence(line)
            for sub in sub_sent:
                if len(sub) > 1:
                    self.__model.topics.append(sub)
        file.close()