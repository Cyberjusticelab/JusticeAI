import copy
from src.fact_extraction.GlobalVariables.regex import Regex
from src.fact_extraction.FactTree import TreeBuilder
from src.fact_extraction.Models import logic


class Pipeline():
    def __init__(self):
        self.__current_clause = [[0, 0]]
        self.__tree_lst = [[]]
        self.__logic_dict = {}
        self.reset_dict()
        self.predicate_lst = []

    def reset_dict(self):
        self.__logic_dict = {}

    def get_logic_dict(self):
        return self.__logic_dict

    def pipe(self, sentence):
        self.__current_clause = [[0, 0]]
        self.__word_dict = {}
        self.__tag_lst = []
        self.__token_lst = []
        self.__group_index = 0
        self.__word_lst = []

        self.__logic_dict.clear()
        self.__group_index = 0
        self.__word_dict[None] = None

        self.classify_words()


    def get_predicate_lst(self):
        tmp_lst = []
        for p in self.predicate_lst:
            if p.predicate.get_word() is None:
                pass
            else:
                tmp_lst.append(p)
        return tmp_lst

    def append_clause(self, height, group):
        h = self.__current_clause[len(self.__current_clause) -1][0]
        g = self.__current_clause[len(self.__current_clause) -1][1]
        if (h != height) or (g != group):
            self.__current_clause.append([height, group])

    def classify_words(self):
        force_cmp = False
        for words in self.__word_lst:
            group = words[0]
            tree_height = words[1]
            phrase = words[2]
            tag = words[3]
            word = words[4]
            dict = self.__logic_dict
            current_clause = self.__current_clause[len(self.__current_clause) - 1][0]
            group_clause = self.__current_clause[len(self.__current_clause) - 1][1]

            if Regex.noun_phrase_match.match(phrase):
                self.add_key_to_dict(dict, tree_height)

                if (current_clause == tree_height) and (group != group_clause):
                    model = logic.LogicModel()
                    past_model = copy.deepcopy(dict[tree_height].previous)
                    model.compliment = past_model.clause
                    model.predicate = past_model.predicate
                    dict[tree_height] = model
                    self.predicate_lst.append(model)
                    self.append_clause(tree_height, group)
                    force_cmp = True

                if Regex.noun_match.match(tag):
                    if (current_clause > 0) and (current_clause < tree_height):
                        dict[current_clause].compliment = dict[tree_height].clause
                        dict[tree_height].clause.set_word(word)

                    else:
                        dict[tree_height].clause.set_word(word)

                    self.append_clause(tree_height, group)

                elif Regex.adjective_match.match(tag):
                    model = dict[tree_height]
                    model.clause.add_qualifier(word)

                elif Regex.determiner_match.match(tag):
                    model = dict[tree_height]
                    model.clause.set_quantifier(word)

            elif Regex.verb_phrase_match.match(phrase):
                self.add_key_to_dict(dict, tree_height)
                if Regex.verb_match.match(tag):
                    dict[tree_height].predicate.set_word(word)

                elif Regex.adjective_match.match(tag):
                    dict[current_clause].compliment.set_word(word)

                elif Regex.adverb_match.match(tag):
                    dict[tree_height].predicate.add_qualifier(word)

            elif Regex.prepositoinal_phrase_match.match(phrase):
                if Regex.verb_match.match(tag):
                    dict[current_clause].predicate.set_word(word)

            elif  Regex.w_word_match.match(tag):
                try:
                    dict[current_clause].predicate.set_word(word)
                except:
                    self.add_key_to_dict(dict, tree_height)
                    dict[tree_height].predicate.set_word(word)

            elif Regex.adjective_phrase_match.match(phrase):
                if Regex.adjective_match.match(tag):
                    dict[current_clause].compliment.set_word(word)

            elif Regex.adverb_phrase_match.match(phrase):
                if Regex.adverb_match.match(tag):
                    dict[current_clause].predicate.add_qualifier(word)

    def add_key_to_dict(self, dict, key):
        try:
            model = dict[key]
        except:
            model = logic.LogicModel()
            dict[key] = model
            self.predicate_lst.append(model)
        try:
            previous_clause = self.__current_clause[len(self.__current_clause) - 2][0]
            model = dict[key]
            model.previous = dict[previous_clause]
            dict[previous_clause].next = model
        except:
            pass




if __name__ == '__main__':
    pipe = Pipeline()
    sentence = "My name is Samuel or my name is Campbell"
    tree = pipe.pipe(sentence)
    dict = pipe.get_predicate_lst()
    for elements in dict:
        print(elements)
        print('---------------------')

