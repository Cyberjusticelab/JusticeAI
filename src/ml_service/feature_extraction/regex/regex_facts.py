# -*- coding: utf-8 -*-
from global_variables.global_variable import Global
import os
from feature_extraction.regex.regex_lib import RegexLib
import numpy
from outputs.output import Save, Log
from sys import stdout
import re


class TagEnum:
    DEMAND = 0
    FACT = 1


class TagPrecedents:
    empty_line_length = 6
    __factMatch = re.compile('\[\d+\]\s')

    def __init__(self, enum):
        """
        Constructor.
        :param enum: TagEnum --> Init default tagger
        """
        self.fact_dict = {}
        self.lines_tagged = 0
        self.text_tagged = 0
        self.nb_lines = 0
        self.nb_text = 0

        if enum == TagEnum.DEMAND:
            self.tagger = RegexLib.regex_demands
            self.model_name = 'demand_matrix'
        else:
            self.tagger = RegexLib.regex_facts
            self.model_name = 'fact_matrix'

    def get_intent_indice(self):
        """
        :return: primary key of every intent in a tuple (int, string)
        """
        return_list = []
        for i in range(len(self.tagger)):
            return_list.append((i, self.tagger[i][0]))
        return return_list

    def tag_precedents(self, nb_files=-1):
        """
        Reads all precedents in a directory
        :param nb_files when -1 then read all directory
        :return: numpy matrix of facts
        """
        Log.write('Tagging precedents')
        count = 0
        for file in os.listdir(Global.precedent_directory):
            if count > 20:
                break
            count += 1
            if nb_files == -1:
                percent = float(
                    self.nb_text / len(os.listdir(Global.precedent_directory))) * 100
            else:
                percent = float(self.nb_text / nb_files) * 100
                if self.nb_text > nb_files:
                    break
            stdout.write("\rPrecedents taged: %f " % percent)
            stdout.flush()
            self.fact_dict[file] = self.__tag_file(file)
            self.nb_text += 1
        Log.write('Precedent coverage: ' +
                  str(self.text_tagged / self.nb_text))
        Log.write('Line Coverage: ' + str(self.lines_tagged / self.nb_lines))
        save = Save('tag_matrix_dir')
        save.binarize_model(self.model_name, self.fact_dict)
        return self.fact_dict

    def __tag_file(self, filename):
        """
        For every line in a precedent, tag facts
        When fact is found then its index is set to 1
        increments text tagged, line tagges to get a percentage
        of coverage at the end of the process
        :param filename: string
        :return: numpy vector of facts
        """
        fact_vector = numpy.zeros(len(self.tagger))
        file = open(Global.precedent_directory + "/" +
                    filename, 'r', encoding="ISO-8859-1")
        text_tagged = False
        for line in file:
            if self.__ignore_line(line):
                continue
            line_tagged = False
            self.nb_lines += 1
            for i in range(len(self.tagger)):
                for regex_value in self.tagger[i][1]:
                    if regex_value.search(line):
                        fact_vector[i] = 1
                        line_tagged = True
                        text_tagged = True

            if line_tagged:
                self.lines_tagged += 1
        if text_tagged:
            self.text_tagged += 1
        return fact_vector

    def __ignore_line(self, line):
        """
        Verifies if we should ignore line from total count
        Add constraints to make covered lines more realistic
        :param line: String
        :return: Boolean
        """
        if len(line) < self.empty_line_length:
            return True
        elif 'No dossier' in line:
            return True
        return False


if __name__ == '__main__':
    # Models saved to ml_service/output/tag_matrix_dir/
    tag = TagPrecedents(TagEnum.FACT)
    dict = tag.tag_precedents()
    # prints fact intents
    print(tag.get_intent_indice())
    tag = TagPrecedents(TagEnum.DEMAND)
    dict = tag.tag_precedents()
    # prints demand intents
    print(tag.get_intent_indice())
