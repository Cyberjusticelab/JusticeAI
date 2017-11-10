# -*- coding: utf-8 -*-
import re

from nltk.tokenize import word_tokenize

from src.ml_service.word_vectors.FrenchVectors import FrenchVectors

# #################################################
# PRECEDENCE MODEL


class PrecedenceModel:
    extra_parse = re.compile("l'")

    # #################################################
    # CONSTRUCTOR
    def __init__(self):
        self.dict = {
            'facts': {
            },
            'decisions': {
            }
        }

    def __str__(self):
        return_str = "Facts:\n"
        for f in self.dict['facts']:
            return_str += str(self.dict['facts'][f])
            return_str += f + '\n\n'

        return_str += 'Decisions:\n'
        for f in self.dict['decisions']:
            return_str += str(self.dict['decisions'][f])
            return_str += f + "\n\n"
        return return_str


class FactModel:
    def __init__(self):
        self.dict = {
            'fact': None,
            'precedence': [],
            'piped_fact': None,
            'vector': None
        }

    def __str__(self):
        return str(self.dict['precedence']) + '\n' + \
            str(self.dict['piped_fact']) + '\n' + \
            str(self.dict['fact'])
