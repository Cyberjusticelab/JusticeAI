import re
import os
from util.models.meta_dict import MetaDict
from util.models.regex_model import RegexModel
from util.models.synonym_model import SynonymModel
from util.models.common_example_model import CommonExampleModel
import sys
import json


class StateEnum:
    NONE = 0
    META = 1
    REGEX = 2
    SYNONYM = 3
    TEXT = 4


class CreateJson:
    META_HEADER = re.compile('\[meta\]')
    REGEX_FEATURES_HEADER = re.compile('\[regex_features\]')
    ENTITY_SYNONYM_HEADER = re.compile('\[entity_synonyms\]')
    TEXT_HEADER = re.compile('\[common_examples:.*\]')
    EMPTY_LINE = re.compile('\s*')
    COMMENTED_LINE = re.compile('^#')

    nlu_dict = {"rasa_nlu_data":
        {
            "regex_features": [

            ],
            "common_examples": [

            ]
        }
    }

    def __init__(self):
        self.current_intent = ""
        self.meta_list = []
        self.regex_list = []
        self.synonym_list = []
        self.intent_list = []

    def reset(self):
        self.current_intent = ""
        self.meta_list = []
        self.regex_list = []
        self.synonym_list = []
        self.intent_list = []
        self.meta_string = ""

    """
    Takes a directory of text files and converts them to JSON files for RASA NLU training.
    read_dir: Directory with txt files to be converted to JSON.
    save_dir: Directory in which to save the converted JSON files. File names will be same as the source text files.
    """

    def parse_directory(self, read_dir, save_dir):
        read_dir = os.getcwd() + read_dir
        save_dir = os.getcwd() + save_dir

        print("RASA Json Creator - Parse Directory\n\t-Read Directory: {}\n\t-Save Directory: {}".format(read_dir,
                                                                                                         save_dir))

        if not os.path.exists(os.path.dirname(save_dir)):
            print("\t!Directory {} does not exist, creating it".format(save_dir))
            os.makedirs(os.path.dirname(save_dir))

        for file in os.listdir(read_dir):
            self.reset()
            with open(read_dir + file, "r") as myfile:
                text = myfile.read()

            self.parse_file(text)
            self.nlu_dict['rasa_nlu_data']['regex_features'] = self.regex_list
            self.nlu_dict['rasa_nlu_data']['common_examples'] = self.intent_list

            filename = save_dir + file.split('.')[0] + '.json'
            with open(filename, 'w+') as fp:
                json.dump(self.nlu_dict, fp)
                print("\t+Writing file: {}".format(filename))

    """
    Takes a single input text file to use as a base and creates JSON files for RASA NLU training for each file in the output file list.
    input_file: Input text file to be used as the base.
    output_file_names: A list of names for the output files. All files will have identical training data.
    save_dir: Directory in which to save the JSON files. File names will be taken from the output file name list.
    """

    def identical_fact_list(self, input_file, output_file_names, save_dir):
        input_file = os.getcwd() + "/" + input_file
        save_dir = os.getcwd() + save_dir

        print(
            "RASA Json Creator - Identical Fact List\n\t-Input File: {}\n\t-Output File Names: {}\n\t-Save Directory: {}"
                .format(input_file, output_file_names, save_dir))

        if not os.path.exists(os.path.dirname(save_dir)):
            print("\t!Directory {} does not exist, creating it".format(save_dir))
            os.makedirs(os.path.dirname(save_dir))

        self.reset()
        with open(input_file) as file:
            text = file.read()

            self.parse_file(text)
            self.nlu_dict['rasa_nlu_data']['regex_features'] = self.regex_list
            self.nlu_dict['rasa_nlu_data']['common_examples'] = self.intent_list

            for filename in output_file_names:
                full_filename = save_dir + filename + '.json'
                with open(full_filename, 'w+') as output_file:
                    json.dump(self.nlu_dict, output_file)
                    print("\t+Writing file: {}".format(full_filename))

    def parse_file(self, file):
        self.state = StateEnum.NONE
        lines = file.split("\n")

        for line in lines:
            if self.META_HEADER.search(line):
                self.state = StateEnum.META

            elif self.REGEX_FEATURES_HEADER.search(line):
                self.state = StateEnum.REGEX

            elif self.ENTITY_SYNONYM_HEADER.search(line):
                self.state = StateEnum.SYNONYM

            elif self.TEXT_HEADER.search(line):
                intent = line.split(": ")[1]
                self.current_intent = intent.replace("]", "")
                self.state = StateEnum.TEXT

            elif len(line) < 5:
                pass

            elif self.COMMENTED_LINE.search(line):
                pass

            elif self.state == StateEnum.META:
                self.meta_list.append(self.find_meta_characters(line))

            elif self.state == StateEnum.REGEX:
                self.regex_list.append(self.find_regex(line))

            elif self.state == StateEnum.SYNONYM:
                self.synonym_list.append(self.find_synonyms(line))

            elif self.state == StateEnum.TEXT:
                self.intent_list.append(self.find_text(line))

    def find_meta_characters(self, line):
        meta_dict = MetaDict()

        meta_characters = line.split('=')[0]
        meta_characters = meta_characters.replace(" ", "")
        meta_dict.open(meta_characters[0])
        meta_dict.close(meta_characters[1])

        meta_meaning = line.split('=')[1]
        meta_meaning = meta_meaning.replace(" ", "")
        if ',' in meta_meaning:
            meta_dict.entity(meta_meaning.split(",")[0])
            meta_dict.extractor(meta_meaning.split(",")[1])
        else:
            meta_dict.entity(meta_meaning)
        return meta_dict.meta

    def find_regex(self, line):
        reg_dict = RegexModel()
        reg_dict.name(line.split(": ")[0])
        reg_dict.pattern(line.split(": ")[1])
        return reg_dict.regex_dict

    def find_synonyms(self, line):
        syn_dict = SynonymModel()
        syn_dict.entity(line.split(": ")[0])

        synonyms = line.split(": ")[1]
        syn_list = synonyms.split(", ")
        syn_dict.synonyms(syn_list)

        return syn_dict.syn_dict

    def find_text(self, line):
        intent_dict = CommonExampleModel().intent_dict
        text = line
        intent_dict['text'] = text
        intent_dict['intent'] = self.current_intent

        entity_list = []

        for dictionary in self.meta_list:
            if dictionary['open'] in line:
                start = text.find(dictionary['open'])
                text = text.replace(dictionary['open'], "", 1)
                end = text.find(dictionary['close'])
                text = text.replace(dictionary['close'], "", 1)
                value = text[start:end]
                entity = dictionary['entity']
                try:
                    extractor = dictionary['extractor']
                except KeyError:
                    extractor = ""

                ent_dict = {
                    "start": start,
                    "end": end,
                    "value": value,
                    "entity": entity,
                }
                if extractor is not "":
                    ent_dict['extractor'] = extractor

                entity_list.append(ent_dict)

        intent_dict['entities'] = entity_list
        intent_dict['text'] = text
        return intent_dict


if __name__ == '__main__':
    read_directory = sys.argv[1]
    save_directory = sys.argv[2]
    parser = CreateJson()
    parser.parse_directory(read_directory, save_directory)
