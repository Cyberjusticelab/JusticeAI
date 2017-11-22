# -*- coding: utf-8 -*-
from global_variables.global_variable import Global
import os
from feature_extraction.regex.regex_lib import RegexLib
import numpy
from outputs.output import Save, Log
from sys import stdout


class TagPrecedents:
    empty_line_length = 6

    def __init__(self):
        self.fact_dict = {}
        self.statements_tagged = 0
        self.text_tagged = 0
        self.nb_lines = 0
        self.nb_text = 0

    def get_intent_indice(self):
        """
        :return: primary key of every intent in a tuple (int, string)
        """
        facts_vector = []
        for i in range(len(RegexLib.regex_facts)):
            facts_vector.append((i, RegexLib.regex_facts[i][0]))

        demands_vector = []
        for i in range(len(RegexLib.regex_demands)):
            demands_vector.append((i, RegexLib.regex_demands[i][0]))

        return {'facts_vector': facts_vector, 'demands_vector': demands_vector}

    def tag_precedents(self, nb_files=-1):
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
        Log.write('Line Coverage: ' +
                  str(self.statements_tagged / self.nb_lines))
        save = Save('precedent_vectors')
        save.binarize_model('precedents_dict.bin', self.fact_dict)
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
        facts_vector = numpy.zeros(len(RegexLib.regex_facts))
        demands_vector = numpy.zeros(len(RegexLib.regex_demands))
        file = open(Global.precedent_directory + "/" +
                    filename, 'r', encoding="ISO-8859-1")
        text_tagged = False
        file_contents = file.read()
        statement_tagged = False
        self.nb_lines += len(file_contents.split('\n'))
        for i, (_, regex_array) in enumerate(RegexLib.regex_facts):
            if self.__match_any_regex(file_contents, regex_array):
                facts_vector[i] = 1
                statement_tagged = True
                text_tagged = True
        for i, (_, regex_array) in enumerate(RegexLib.regex_demands):
            if self.__match_any_regex(file_contents, regex_array):
                demands_vector[i] = 1
                statement_tagged = True
                text_tagged = True
        if statement_tagged:
            self.statements_tagged += 1
        file.close()
        if text_tagged:
            self.text_tagged += 1
        return {'facts_vector': facts_vector, 'demands_vector': demands_vector}

    def __match_any_regex(self, text, regex_array):
        """
            Returns True if any of the regex in regex_array
            are found in the given text string
        """
        for regex_value in regex_array:
            if regex_value.search(text):
                return True

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
    dict = tag.tag_precedents(1000)
    # prints fact intents
    indices = tag.get_intent_indice()

    print("Total precedents parsed: {}".format(len(tag.fact_dict)))
    for i in range(len(next(iter(tag.fact_dict.values()))['facts_vector'])):
        total_fact = len([1 for val in tag.fact_dict.values()
                          if val['facts_vector'][i] == 1])
        print("Total precedents with {:41} : {}".format(
            indices['facts_vector'][i][1], total_fact))
    for i in range(len(next(iter(tag.fact_dict.values()))['demands_vector'])):
        total_fact = len([1 for val in tag.fact_dict.values()
                          if val['demands_vector'][i] == 1])
        print("Total precedents with {:41} : {}".format(
            indices['demands_vector'][i][1], total_fact))
