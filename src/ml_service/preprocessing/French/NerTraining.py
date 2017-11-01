# -*- coding: utf-8 -*-
import os
import pickle
import re
import string

import nltk
import numpy

from src.ml_service.preprocessing.French.Vectorize import FrenchVectors
from src.ml_service.preprocessing.French.GlobalVariable import Global


class Ner:
    entity_labels = {
        'Time': [],
        'Date': [],
        'Money': [],
        'Time_Frequency': [],
        'Relative_Time': [],
        'Other': []
    }

    # #################################################
    # CONSTRUCTOR
    def __init__(self):
        self.fv = FrenchVectors()

    # #################################################
    # TRAIN NAMED ENTITY
    # -------------------------------------------------
    # Main method. Just run with a window size and
    # model will be saved in same directory
    # window: int
    def train_named_entity(self, window=0):
        tuple_list = []
        tokens_list = []
        tokens = None

        script_dir = os.path.dirname(__file__)
        rel_path = r"french_data/"
        abs_file_path = os.path.join(script_dir, rel_path)

        for i in os.listdir(abs_file_path):
            if '.ann' in i:
                text = i.split('.')[0] + '.txt'

                with open(abs_file_path + text, 'r') as content_file:
                    content = content_file.read()

                tokens = nltk.word_tokenize(content)
                tokens_list.append(tokens)
                tpl = self.__form_tuple(i)
                tuple_list.append(tpl)
                tokens = self.__annotate_raw_text(content, tpl)
            self.__populate_entities(tokens, window)
        self.__create_vectors()
        self.__save_pickle()
        print("Training complete")

    # #################################################
    # FORM TUPLE
    # -------------------------------------------------
    # Forms tuple:
    # ("november", "date")
    # ("in 1 hour", "time")
    def __form_tuple(self, filename):
        tuple_list = []

        script_dir = os.path.dirname(__file__)
        rel_path = r"french_data/" + filename
        abs_file_path = os.path.join(script_dir, rel_path)

        file = open(abs_file_path, 'r', encoding="ISO-8859-1")
        for lines in file:
            word_ent = self.__get_word_entity(lines)
            tokens = nltk.word_tokenize(word_ent[1])
            for t in tokens:
                tuple_list.append((word_ent, t))
        file.close()

        return tuple_list

    # #################################################
    # GET WORD ENTITY
    # -------------------------------------------------
    # Extract word entity from start:end index in text
    def __get_word_entity(self, lines):
        line = lines.split('\t')
        entity = line[1].split(" ")
        word = line[2].replace("\n", "")
        word = word.encode("ISO-8859-1")
        word = word.decode("utf-8")
        return entity[0], word, self.__get_span(entity)

    # #################################################
    # GET SPAN
    # -------------------------------------------------
    # Span is the start and end index of a word
    # returns: (int, int)
    def __get_span(self, entity):
        try:
            return int(entity[1]), int(entity[2])
        except:
            return int(entity[1]), int(entity[3])

    # #################################################
    # ANNOTATE RAW TEXT
    # -------------------------------------------------
    # Long complicated method. please just trust.
    # Will essentially annotate the entire text in
    # tuple form. The corpus only annotates key words
    # but for this algorithm I decided to annotate
    # every single word. None-key words are 'Other'
    def __annotate_raw_text(self, text, tuple_list):
        return_list = []
        tuple_list.sort(key=lambda x: x[0][2][0], reverse=True)
        text = text.replace(",", " ")
        text = text.replace("'", " ")
        for i in range(len(tuple_list)):
            span = tuple_list[i][0][2]
            start = span[0]
            end = span[1]
            try:
                if text[start + 1] == "(":
                    continue
                elif text[start] == "(":
                    continue
            except IndexError:
                pass
            text = text[:end] + ';' + tuple_list[i][0][0] + ")" + text[end:]
            text = text[:start] + "(" + text[start:]
        text = text.replace("\n", " ")
        tokens = text.split(" ")
        for i in range(len(tokens)):
            if tokens[i] == "":
                pass
            elif tokens[i][0] == '(':
                tokens[i] = tokens[i].replace("(", "")
                tokens[i] = tokens[i].replace(")", "")
                tpl = tokens[i].split(';')
                try:
                    return_list.append((tpl[0], tpl[1]))
                except:
                    pass
            else:
                return_list.append((tokens[i], 'Other'))
        return return_list

    # #################################################
    # CREATE VECTORS
    def __create_vectors(self):
        for entity in self.entity_labels:
            vec_sum = numpy.zeros(500)
            lst = self.entity_labels[entity]

            for vectors in lst:
                vec_sum = numpy.add(vec_sum, vectors)

            self.entity_labels[entity] = numpy.divide(vec_sum, len(lst))

    # #################################################
    # POPULATE LABELS
    def __populate_entities(self, token_list, window):
        for i in range(len(token_list)):
            try:
                vec = self.__vectorize_word_window(token_list, i, window)
                if vec is not None:
                    self.entity_labels[token_list[i][1]].append(vec)
            except KeyError:
                pass

    # #################################################
    # VECTORIZE WINDOW
    def __vectorize_word_window(self, token_list, index, window):
        num_words = 0
        vec_sum = numpy.zeros(500)
        for i in range(index - window, index + window + 1, 1):
            try:
                word = token_list[i][0].lower()
                word = re.sub('[' + string.punctuation + ']', '', word)
                if word in Global.custom_stop_words:
                    continue
                if token_list[i][1] == 'Money':
                    word = '$'
            except IndexError:
                continue
            try:
                vec_sum = numpy.add(vec_sum, self.fv.word_vectors[word])
                num_words += 1
            except:
                pass
        if num_words == 0:
            return None
        return numpy.divide(vec_sum, num_words)

    # #################################################
    # SAVE PICKLE
    def __save_pickle(self):
        script_dir = os.path.dirname(__file__)
        rel_path = r"ner_model.pickle"
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path, 'wb') as f:
            pickle.dump(self.entity_labels, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    ner = Ner()
    ner.train_named_entity(window=1)
