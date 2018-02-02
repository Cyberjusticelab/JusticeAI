# -*- coding: utf-8 -*-
import os
import numpy
from util.file import Save
from util.log import Log
from util.constant import Path
from sys import stdout
from util.file import Load
from feature_extraction.post_processing.regex.regex_entity_extraction import EntityExtraction


class TagPrecedents:
    empty_line_length = 6

    def __init__(self):
        self.precedent_vector = {}
        self.statements_tagged = 0
        self.text_tagged = 0
        self.nb_lines = 0
        self.nb_text = 0
        self.regexes = Load.load_binary("regexes.bin")
        self.precedents_directory_path = Path.raw_data_directory

    def get_intent_index(self):
        """
        Retrieves the label of every column in the vectors

        example: "lease_termination": 0, "tenant_violent": 1 ...

                 [        1            ,          0        , ...]
                 [        1            ,          1        , ...]
                 ...

        :return: primary key of every intent in a tuple (int, string)
        """
        facts_vector = []
        for i in range(len(self.regexes["regex_facts"])):
            name = self.regexes["regex_facts"][i][0]
            if self.regexes["regex_facts"][i][2] == 'BOOLEAN':
                data_type = 'bool'
            else:
                data_type = 'int'
            facts_vector.append((i, name, data_type))

        demands_vector = []
        for i in range(len(self.regexes["regex_demands"])):
            name = self.regexes["regex_demands"][i][0]
            if self.regexes["regex_demands"][i][2] == 'BOOLEAN':
                data_type = 'bool'
            else:
                data_type = 'int'
            demands_vector.append((i, name, data_type))

        outcomes_vector = []
        for i in range(len(self.regexes["regex_outcomes"])):
            name = self.regexes["regex_outcomes"][i][0]
            if self.regexes["regex_outcomes"][i][2] == 'BOOLEAN':
                data_type = 'bool'
            else:
                data_type = 'int'
            outcomes_vector.append((i, name, data_type))

        return {
            'facts_vector': facts_vector,
            'demands_vector': demands_vector,
            'outcomes_vector': outcomes_vector
        }

    def tag_precedents(self, nb_files=-1):
        """
        1) Displays progress of files vectorized
        2) Vectorize file
        3) Displays percentage of files covered
        4) displays percentage of lines covered
        5) binarize vectors

        :param nb_files when -1 then read all directory
        :return:
        structured_data_dict:{
            filename:{
                name: 'AZ-XXXXXXX.txt',
                demands_vector: [...],
                facts_vector: [...],
                outcomes_vector: [...]
            }
        }
        """

        # ----------------------- 1 -----------------------------#
        Log.write('Tagging precedents')
        for file in os.listdir(self.precedents_directory_path):
            if nb_files == -1:
                percent = float(
                    self.nb_text / len(os.listdir(self.precedents_directory_path))) * 100
            else:
                percent = float(self.nb_text / nb_files) * 100
                if self.nb_text > nb_files:
                    break
            stdout.write("\rPrecedents taged: %f " % percent)
            stdout.flush()

            # ----------------------- 2 -----------------------------#
            self.precedent_vector[file] = self.__tag_file(file)
            self.nb_text += 1

        # ----------------------- 3 -----------------------------#
        Log.write('Precedent coverage: ' +
                  str(self.text_tagged / self.nb_text))

        # ----------------------- 4 -----------------------------#
        Log.write('Line Coverage: ' +
                  str(self.statements_tagged / self.nb_lines))

        # ----------------------- 5 -----------------------------#
        save = Save()
        save.save_binary('precedent_vectors.bin', self.precedent_vector)
        return self.precedent_vector

    def __tag_file(self, filename):
        """
        1) Create vectors of 0's
        2) Create fact vector
        3) create demands vector
        4) create outcomes vector
        5) updates line / text coverage

        :param filename: string
        :return: {
            'name': filename,
            'facts_vector': facts_vector,
            'demands_vector': demands_vector,
            'outcomes_vector': outcomes_vector
            }
        """

        # ----------------------- 1 -----------------------------#
        facts_vector = numpy.zeros(len(self.regexes["regex_facts"]))
        demands_vector = numpy.zeros(len(self.regexes["regex_demands"]))
        outcomes_vector = numpy.zeros(len(self.regexes["regex_outcomes"]))

        file = open(self.precedents_directory_path + "/" +
                    filename, 'r', encoding="ISO-8859-1")
        text_tagged = False
        file_contents = file.read()
        statement_tagged = False
        self.nb_lines += len(file_contents.split('\n'))

        # ----------------------- 2 -----------------------------#
        for i, (_, regex_array, regex_type) in enumerate(self.regexes["regex_facts"]):
            match = EntityExtraction.match_any_regex(file_contents, regex_array, regex_type)
            if match[0]:
                facts_vector[i] = match[1]
                statement_tagged = True
                text_tagged = True

        # ----------------------- 3 -----------------------------#
        for i, (_, regex_array, regex_type) in enumerate(self.regexes["regex_demands"]):
            match = EntityExtraction.match_any_regex(file_contents, regex_array, regex_type)
            if match[0]:
                demands_vector[i] = match[1]
                statement_tagged = True
                text_tagged = True

        # ----------------------- 4 -----------------------------#
        for i, (_, regex_array, regex_type) in enumerate(self.regexes["regex_outcomes"]):
            match = EntityExtraction.match_any_regex(file_contents, regex_array, regex_type)
            if match[0]:
                outcomes_vector[i] = match[1]
                statement_tagged = True
                text_tagged = True

        # ----------------------- 5 -----------------------------#
        if statement_tagged:
            self.statements_tagged += 1
        file.close()
        if text_tagged:
            self.text_tagged += 1

        return {
            'name': filename,
            'facts_vector': facts_vector,
            'demands_vector': demands_vector,
            'outcomes_vector': outcomes_vector
        }

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


def run(nb_files=-1):
    """
    Models saved to ml_service/data/binary/
    1) create vectors and save them
    2) retrieve the lab
    :return: None
    """

    tag = TagPrecedents()
    precedent_vector = tag.tag_precedents(nb_files)
    # prints fact intents
    indexes = tag.get_intent_index()

    Log.write("Total precedents parsed: {}".format(len(precedent_vector)))
    for i in range(len(next(iter(precedent_vector.values()))['facts_vector'])):
        total_fact = len([1 for val in precedent_vector.values() if val['facts_vector'][i] != 0])
        Log.write("Total precedents with {:41} : {}".format(indexes['facts_vector'][i][1], total_fact))
    Log.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    for i in range(len(next(iter(precedent_vector.values()))['demands_vector'])):
        total_fact = len([1 for val in precedent_vector.values() if val['demands_vector'][i] != 0])
        Log.write("Total precedents with {:41} : {}".format(indexes['demands_vector'][i][1], total_fact))
    Log.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    for i in range(len(next(iter(precedent_vector.values()))['outcomes_vector'])):
        total_fact = len([1 for val in precedent_vector.values() if val['outcomes_vector'][i] != 0])
        Log.write("Total precedents with {:41} : {}".format(indexes['outcomes_vector'][i][1], total_fact))
    Log.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
