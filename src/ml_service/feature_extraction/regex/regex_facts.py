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

    def __init__(self):
        """
        Constructor.
        :param enum: TagEnum --> Init default tagger
        """
        self.fact_dict = {}
        self.lines_tagged = 0
        self.text_tagged = 0
        self.nb_lines = 0
        self.nb_text = 0

    def get_intent_indice(self):
        """
        :return: primary key of every intent in a tuple (int, string)
        """
        fact_list = []
        demand_list = []
        for i in range(len(RegexLib.regex_facts)):
            fact_list.append((i, RegexLib.regex_facts[i][0]))
        fact_list = []
        for i in range(len(RegexLib.regex_demands)):
            demand_list.append((i, RegexLib.regex_demands[i][0]))

        return {'fact_list' : fact_list, 'demand_list' : demand_list}

    def tag_precedents(self, nb_files=100):
        """
        Reads all precedents in a directory
        :param nb_files when -1 then read all directory
        :return: numpy matrix of facts
        """
        Log.write('Tagging precedents')
        for file in os.listdir(Global.precedent_directory):
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
        save.binarize_model('precedent_dict', self.fact_dict)
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
        fact_vector = numpy.zeros(len(RegexLib.regex_facts))
        demand_vector = numpy.zeros(len(RegexLib.regex_demands))
        file = open(Global.precedent_directory + "/" +
                    filename, 'r', encoding="ISO-8859-1")
        text_tagged = False

        for line in file:
            if self.__ignore_line(line):
                continue
            line_tagged = False
            self.nb_lines += 1
            for i, (_, regex_array) in enumerate(RegexLib.regex_facts):
                for regex_value in regex_array:
                    if regex_value.search(line):
                        fact_vector[i] = 1
                        line_tagged = True
                        text_tagged = True
                        print(self.lines_tagged)
                        break
            for i, (_, regex_array) in enumerate(RegexLib.regex_demands):
                for regex_value in regex_array:
                    if regex_value.search(line):
                        fact_vector[i] = 1
                        line_tagged = True
                        text_tagged = True
                        break
            if line_tagged:
                self.lines_tagged += 1
        file.close()
        if text_tagged:
            self.text_tagged += 1
        return {'fact_vector' : fact_vector, 'demand_vector' : demand_vector}

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
    tag = TagPrecedents()
    dict = tag.tag_precedents()
    # prints fact intents
    print(tag.get_intent_indice())
