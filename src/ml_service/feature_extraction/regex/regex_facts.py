# -*- coding: utf-8 -*-
from global_variables.global_variable import Global
import os
from feature_extraction.regex.regex_lib import RegexLib
import numpy
from outputs.output import Save, Log
from sys import stdout


class RegexFacts:
    empty_line_length = 6

    def __init__(self):
        self.fact_matrix = []
        self.lines_tagged = 0
        self.text_tagged = 0
        self.nb_lines = 0
        self.nb_text = 0

    def tag_precedents(self, nb_files=-1):
        """
        Reads all precedents in a directory
        :return: numpy matrix of facts
        """
        Log.write('Tagging precedents')

        for file in os.listdir(Global.precedent_directory):
            if nb_files == -1:
                percent = float(self.nb_text / len(os.listdir(Global.precedent_directory))) * 100
            else:
                percent = float(self.nb_text / nb_files) * 100
                if self.nb_text > nb_files:
                    break
            stdout.write("\rPrecedents taged: %f " % percent)
            stdout.flush()
            self.fact_matrix.append(self.__tag_file(file))
            self.nb_text += 1
        print()
        Log.write('Precedent coverage: ' + str(float(self.text_tagged / self.nb_text)))
        Log.write('Line Coverage: ' + str(float(self.lines_tagged / self.nb_lines)))
        save = Save('fact_matrix_dir')
        save.binarize_model('fact_matrix', self.fact_matrix)

    def __tag_file(self, filename):
        """
        For every line in a precedent, tag facts
        When fact is found then its index is set to 1
        increments text tagged, line tagges to get a percentage
        of coverage at the end of the process
        :param filename:
        :return: numpy vector of facts
        """
        fact_vector = numpy.full(len(RegexLib.regex_list), -1)
        file = open(Global.precedent_directory + "/" + filename, 'r', encoding="ISO-8859-1")
        text_tagged = False
        for line in file:
            if len(line) < self.empty_line_length:
                continue
            line_tagged = False
            self.nb_lines += 1
            for i in range(len(RegexLib.regex_list)):
                # we will assume a NOT(fact) will be it's own column for now
                # so no 0 in vector as of yet only -1 and 1
                if RegexLib.regex_list[i].match(line):
                    fact_vector[i] = 1
                    line_tagged = True
                    text_tagged = True
            if line_tagged:
                self.lines_tagged += 1
        if text_tagged:
            self.text_tagged += 1
        return fact_vector


if __name__ == '__main__':
    re_facts = RegexFacts()
    re_facts.tag_precedents()
