from bllipparser import RerankingParser
from bllipparser.ModelFetcher import download_and_install_model
import nltk
import re
from src.fact_extraction import Model, clause, compliment, predicate
import copy
class Pipeline():
    phrase_match = re.compile('ADJP|PP|ADVP|NP|S|SQ|SBARQ|VP')
    noun_match = re.compile('NN|PRP|PRP$|CC')
    noun_phrase_match = re.compile('NP')
    verb_match = re.compile('VB|IN|TO')
    w_word_match = re.compile('WRB')
    verb_phrase_match = re.compile('VP|WHADVP')
    adjective_match = re.compile('JJ|CC')
    determiner_match = re.compile('DT|EX')
    adjective_phrase_match = re.compile('ADJP')
    prepositoinal_phrase_match = re.compile('PP')
    conjunction_match = re.compile('CC')
    adverb_match = re.compile('RB')
    adverb_phrase_match = re.compile('ADVP')


    def __init__(self):
        self.__current_clause = [[0, 0]]
        self.__word_dict = {}
        self.__tag_lst = []
        self.__token_lst = []
        model_dir = download_and_install_model('WSJ', '/tmp/models')
        # Loading the model is slow, but only needs to be done once
        self.__rpp = RerankingParser.from_unified_model_dir(model_dir)
        self.__tree_lst = [[]]
        self.__group_index = 0
        self.__logic_dict = {}
        self.reset_dict()
        self.__word_lst = []
        self.predicate_lst = []

    def reset_dict(self):
        self.__logic_dict = {}

    def get_logic_dict(self):
        return self.__logic_dict

    def pipe(self, sentence):

        self.__tag_lst.clear()
        self.__token_lst.clear()
        self.__word_dict.clear()
        self.__current_clause = [[0, 0]]
        self.__word_dict = {}
        self.__tag_lst = []
        self.__token_lst = []
        self.__group_index = 0
        self.__word_lst = []

        self.__logic_dict.clear()
        self.__group_index = 0
        self.__word_dict[None] = None
        nbest_list = self.__rpp.parse(sentence)
        nbest_list = nbest_list.fuse()
        self.tree = nbest_list.subtrees()
        tree = nbest_list.as_nltk_tree()
        tree.draw()
        self.__traverse_tree(tree, self.__tag_lst, self.__token_lst)
        self.classify_words()

    def get_tag_lst(self):
        return self.__tag_lst.copy()

    def get_token_lst(self):
        return self.__token_lst.copy()

    def get_word_dict(self):
        return self.__word_dict
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

            if self.noun_phrase_match.match(phrase):
                self.add_key_to_dict(dict, tree_height)

                if (current_clause == tree_height) and (group != group_clause):
                    model = Model.Logic_Model()
                    past_model = copy.deepcopy(dict[tree_height].previous)
                    model.compliment = past_model.clause
                    model.predicate = past_model.predicate
                    dict[tree_height] = model
                    self.predicate_lst.append(model)
                    self.append_clause(tree_height, group)
                    force_cmp = True

                if self.noun_match.match(tag):
                    if (current_clause > 0) and (current_clause < tree_height):
                        dict[current_clause].compliment = dict[tree_height].clause
                        dict[tree_height].clause.set_word(word)

                    else:
                        dict[tree_height].clause.set_word(word)

                    self.append_clause(tree_height, group)

                elif self.adjective_match.match(tag):
                    model = dict[tree_height]
                    model.clause.add_qualifier(word)

                elif self.determiner_match.match(tag):
                    model = dict[tree_height]
                    model.clause.set_quantifier(word)

            elif self.verb_phrase_match.match(phrase):
                self.add_key_to_dict(dict, tree_height)
                if self.verb_match.match(tag):
                    dict[tree_height].predicate.set_word(word)

                elif self.adjective_match.match(tag):
                    dict[current_clause].compliment.set_word(word)

                elif self.adverb_match.match(tag):
                    dict[tree_height].predicate.add_qualifier(word)

            elif self.prepositoinal_phrase_match.match(phrase):
                if self.verb_match.match(tag):
                    dict[current_clause].predicate.set_word(word)

            elif self.w_word_match.match(tag):
                try:
                    dict[current_clause].predicate.set_word(word)
                except:
                    self.add_key_to_dict(dict, tree_height)
                    dict[tree_height].predicate.set_word(word)

            elif self.adjective_phrase_match.match(phrase):
                if self.adjective_match.match(tag):
                    dict[current_clause].compliment.set_word(word)

            elif self.adverb_phrase_match.match(phrase):
                if self.adverb_match.match(tag):
                    dict[current_clause].predicate.add_qualifier(word)

    def add_key_to_dict(self, dict, key):
        try:
            model = dict[key]
        except:
            model = Model.Logic_Model()
            dict[key] = model
            self.predicate_lst.append(model)
        try:
            previous_clause = self.__current_clause[len(self.__current_clause) - 2][0]
            model = dict[key]
            model.previous = dict[previous_clause]
            dict[previous_clause].next = model
        except:
            pass

    def __traverse_tree(self, tree, tag_lst, token_lst, depth = 0, phrase_type = None):
        for subtree in tree:
            if type(subtree) == nltk.tree.Tree:
                if self.phrase_match.match(subtree.label()):
                    new_tag_lst = [(depth, subtree.label())]
                    tag_lst.append(new_tag_lst)
                    new_token_lst = [subtree.label()]

                    d = depth + 1

                    token_lst.append(new_token_lst)
                    self.__group_index = self.__group_index + 1
                    self.__traverse_tree(subtree, new_tag_lst, new_token_lst, d, subtree.label())
                else:
                    tag_lst.append(subtree.label())
                    token_lst.append(subtree.leaves()[0])
                    self.__word_dict[self.__group_index] = (depth, phrase_type, subtree.label(), subtree.leaves()[0])
                    self.__word_lst.append((self.__group_index, depth, str(phrase_type), subtree.label(), subtree.leaves()[0]))
                    self.__traverse_tree(subtree, tag_lst, token_lst)


if __name__ == '__main__':
    pipe = Pipeline()
    sentence = "My name is Samuel or my name is Campbell"
    tree = pipe.pipe(sentence)
    dict = pipe.get_predicate_lst()
    for elements in dict:
        print(elements)
        print('---------------------')

