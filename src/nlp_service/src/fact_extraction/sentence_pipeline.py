from bllipparser import RerankingParser
from bllipparser.ModelFetcher import download_and_install_model
import nltk
import re
from src.fact_extraction import Model, clause, compliment, predicate

class Pipeline():
    phrase_match = re.compile('ADJP|PP|ADVP|NP|S|SQ|SBARQ|VP')
    noun_match = re.compile('NN|PRP|PRP$')
    noun_phrase_match = re.compile('NP')
    verb_match = re.compile('VB|IN|TO')
    w_word_match = re.compile('WRB')
    verb_phrase_match = re.compile('VP|WHADVP')
    adjective_match = re.compile('JJ')
    determiner_match = re.compile('DT|EX')
    adjective_phrase_match = re.compile('ADJP')
    prepositoinal_phrase_match = re.compile('PP')


    def __init__(self):
        self.__current_clause = 0
        self.__word_dict = {}
        self.__tag_lst = []
        self.__token_lst = []
        model_dir = download_and_install_model('WSJ', '/tmp/models')
        # Loading the model is slow, but only needs to be done once
        self.__rpp = RerankingParser.from_unified_model_dir(model_dir)
        self.__tree_lst = [[]]
        self.__word_index = 0
        self.__logic_dict = {}
        self.reset_dict()
        self.__word_lst = []

    def reset_dict(self):
        self.__logic_dict = {}

    def get_logic_dict(self):
        return self.__logic_dict

    def pipe(self, sentence):
        self.__word_index = 0
        self.__tag_lst.clear()
        self.__token_lst.clear()
        self.__word_dict.clear()
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

    def classify_words(self):
        for words in self.__word_lst:
            tree_height = words[1]
            phrase = words[2]
            tag = words[3]
            word = words[4]
            dict = self.__logic_dict

            if self.noun_phrase_match.match(phrase):
                self.add_key_to_dict(tree_height)

                if self.noun_match.match(tag):
                    if (self.__current_clause > 0) and (self.__current_clause < tree_height):
                        dict[self.__current_clause].compliment = dict[tree_height].clause
                        dict[tree_height].clause.set_word(word)
                    else:
                        dict[tree_height].clause.set_word(word)

                    self.__current_clause = tree_height

                elif self.adjective_match.match(tag):
                    model = dict[tree_height]
                    model.clause.add_qualifier(word)

                elif self.determiner_match.match(tag):
                    model = dict[tree_height]
                    model.clause.set_quantifier(word)

            elif self.verb_phrase_match.match(phrase):
                self.add_key_to_dict(tree_height)
                if self.verb_match.match(tag):
                    dict[tree_height].predicate.set_word(word)

            elif self.prepositoinal_phrase_match.match(phrase):
                if self.verb_match.match(tag):
                    dict[self.__current_clause].predicate.set_word(word)

            elif self.w_word_match.match(tag):
                try:
                    dict[self.__current_clause].predicate.set_word(word)
                except:
                    self.add_key_to_dict(tree_height)
                    dict[tree_height].predicate.set_word(word)

            elif self.adjective_phrase_match.match(phrase):
                if self.adjective_match.match(tag):
                    dict[self.__current_clause].compliment.set_word(word)


    def add_key_to_dict(self, key):
        dict = self.__logic_dict
        try:
            model = dict[key]
        except:
            model = Model.Logic_Model()
            dict[key] = model

    def __traverse_tree(self, tree, tag_lst, token_lst, depth = 0, phrase_type = None):
        for subtree in tree:
            if type(subtree) == nltk.tree.Tree:
                if self.phrase_match.match(subtree.label()):
                    new_tag_lst = [(depth, subtree.label())]
                    tag_lst.append(new_tag_lst)
                    new_token_lst = [subtree.label()]

                    d = depth + 1

                    token_lst.append(new_token_lst)
                    self.__traverse_tree(subtree, new_tag_lst, new_token_lst, d, subtree.label())
                else:
                    tag_lst.append(subtree.label())
                    token_lst.append(subtree.leaves()[0])
                    self.__word_dict[self.__word_index] = (depth, phrase_type, subtree.label(), subtree.leaves()[0])
                    self.__word_lst.append((self.__word_index, depth, str(phrase_type), subtree.label(), subtree.leaves()[0]))
                    self.__word_index = self.__word_index + 1
                    self.__traverse_tree(subtree, tag_lst, token_lst)


if __name__ == '__main__':
    pipe = Pipeline()
    sentence = "My landlord beat me to death."
    tree = pipe.pipe(sentence)
    dict = pipe.get_logic_dict()
    for elements in dict:
        print(dict[elements])
        print('---------------------')

