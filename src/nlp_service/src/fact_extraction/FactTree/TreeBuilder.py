import nltk
from src.fact_extraction.GlobalVariables.regex import Regex
from bllipparser import RerankingParser
from bllipparser.ModelFetcher import download_and_install_model


class Tree:
    ###################################################
    # CONSTRUCTOR
    # -------------------------------------------------
    # Stores word list, list of word tokens, list of
    # word tags and a dictionary of words
    def __init__(self):
        self.__logic_lst = []
        self.__token_lst = []
        self.__tag_lst = []
        self.__word_lst = []
        model_dir = download_and_install_model('WSJ', '/tmp/models')
        self.__rpp = RerankingParser.from_unified_model_dir(model_dir)

    ###################################################
    # BUILD
    # -------------------------------------------------
    # 1) reset current lists and dictionaries
    # 2) creates tree representing sentence
    # 3) transforms tree to nltk type
    # 4) draw tree
    # 5) traverse tree and populate lists
    #
    # sentence: string
    # draw: boolean
    def build(self, sentence, draw = False):
        self.__reset()
        nbest_list = self.__rpp.parse(sentence)
        nbest_list = nbest_list.fuse()
        self.tree = nbest_list.subtrees()
        tree = nbest_list.as_nltk_tree()
        if draw:
            tree.draw()
        self.__traverse_tree(tree, self.__tag_lst, self.__token_lst)

    ###################################################
    # TRAVERSE
    # -------------------------------------------------
    # - Depth first search of words and tokens
    # - Words are appended to list by order in which they appear
    # - Words are inserted into a tuple
    #   (tree_height, phrase_type, word_type, word)
    #   (int, int, string, string, string)
    #
    # tree: nltk tree
    # tag_lst: lst[]
    # token_lst: lst[]
    # depth: integer
    # phrase_type: string
    def __traverse_tree(self, tree, tag_lst, token_lst, depth=0, phrase_type=None):
        for subtree in tree:
            if type(subtree) == nltk.tree.Tree:
                if Regex.phrase_match.match(subtree.label()):
                    new_tag_lst = [(depth, subtree.label())]
                    tag_lst.append(new_tag_lst)
                    new_token_lst = [subtree.label()]
                    token_lst.append(new_token_lst)
                    self.__traverse_tree(subtree, new_tag_lst, new_token_lst, depth + 1, subtree.label())
                else:
                    word = subtree.leaves()[0]
                    label = subtree.label()
                    tag_lst.append(label)
                    token_lst.append(word)
                    #self.__word_dict[self.__group_index] = (depth, phrase_type, label, word)
                    self.__word_lst.append((depth, str(phrase_type), label, word))
                    self.__traverse_tree(subtree, tag_lst, token_lst)

    def __reset(self):
        self.__word_dict = {}
        self.__token_lst = []
        self.__tag_lst = []
        self.__word_lst = []

    def get_tag_lst(self):
        return self.__tag_lst.copy()

    def get_token_lst(self):
        return self.__token_lst.copy()

    def get_word_lst(self):
        return self.__word_lst.copy()