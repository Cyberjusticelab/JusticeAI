import re
import os
from util.models.meta_dict import MetaDict
from util.models.regex_model import RegexModel
from util.models.synonym_model import SynonymModel
from util.models.common_example_model import CommonExampleModel

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

    def parse_directory(self, directory):
        for file in os.listdir(directory):
            self.reset()
            with open(file, "r") as myfile:
                text = myfile.readlines()
            self.parse_file(text)
            self.nlu_dict['rasa_nlu_data']['regex_features'] += self.regex_list
            self.nlu_dict['rasa_nlu_data']['common_examples'] += self.intent_list

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
        meta_characters = meta_characters.replace(" " , "")
        meta_dict.open(meta_characters[0])
        meta_dict.close(meta_characters[1])

        meta_meaning = line.split('=')[1]
        meta_meaning = meta_meaning.replace(" ", "")
        meta_dict.entity(meta_meaning.split(",")[0])
        meta_dict.extractor(meta_meaning.split(",")[1])

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
                end = text.find(dictionary['close']) - 1
                text = text.replace(dictionary['open'], "")
                text = text.replace(dictionary['close'], "")
                value = text[start:end]
                entity = dictionary['entity']
                extractor = dictionary['extractor']

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