import nltk
from src.fact_extraction.GlobalVariables.regex import Regex
from bllipparser import RerankingParser
from bllipparser.ModelFetcher import download_and_install_model
from src.fact_extraction.Models import compliment, predicate, clause, logic

class Tree:
    ###################################################
    # CONSTRUCTOR
    # -------------------------------------------------
    # Stores word list, list of word tokens, list of
    # word tags and a dictionary of words
    def __init__(self):
        self.__token_lst = []
        self.__tag_lst = []
        self.__word_lst = []
        self.__logic_model = []
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
    # - In parallel, words are also classified and appended to logic list
    #
    # tree: nltk tree
    # tag_lst: lst[]
    # token_lst: lst[]
    # depth: integer
    def __traverse_tree(self, tree, tag_lst, token_lst, depth = 0):
        for subtree in tree:
            if type(subtree) == nltk.tree.Tree:
                if Regex.phrase_match.match(subtree.label()):
                    new_tag_lst = [(depth, subtree.label())]
                    tag_lst.append(new_tag_lst)
                    new_token_lst = [subtree.label()]
                    token_lst.append(new_token_lst)
                    self.__append_logic_object(subtree.label())
                    self.__traverse_tree(subtree, new_tag_lst, new_token_lst, depth + 1)
                else:
                    word = subtree.leaves()[0]
                    label = subtree.label()
                    tag_lst.append(label)
                    token_lst.append(word)
                    self.__define_logic_object(label, word)
                    self.__traverse_tree(subtree, tag_lst, token_lst)

    #####################################
    # RESET
    def __reset(self):
        self.__logic_model = []
        self.__word_dict = {}
        self.__token_lst = []
        self.__tag_lst = []
        self.__word_lst = [[]]

    #####################################
    # GET LOGIC MODEL
    def get_logic_model(self):
        new_list = []
        for elements in self.__logic_model:
            if elements.empty_model():
                pass
            else:
                new_list.append(elements)
        return new_list

    #####################################
    # GET TAG LIST
    def get_tag_lst(self):
        return self.__tag_lst.copy()

    #####################################
    # GET TOKEN LIST
    def get_token_lst(self):
        return self.__token_lst.copy()

    #####################################
    # GET WORD LIST
    def get_word_lst(self):
        return self.__word_lst.copy()

    #####################################
    # DEFINE LOGIC OBJECT
    # -----------------------------------
    # Uses regular expression to match tags
    # from phrases.
    # From the tags we create the appropriate
    # logical feature
    #
    # tag: string
    # word: string
    def __define_logic_object(self, tag, word):
        try:
            model = self.__logic_model[len(self.__logic_model) - 1]
        except IndexError:
            return
        if Regex.noun_match.match(tag):
            model.set_word(word, tag)
        elif Regex.verb_match.match(tag):
            model.set_word(word, tag)
        elif Regex.adjective_match.match(tag):
            if type(model) == compliment.compliment:
                model.set_word(word, tag)
            else:
                model.add_qualifier(word, tag)
        elif Regex.adverb_match.match(tag):
            model.add_qualifier(word, tag)
        elif Regex.conjunction_match.match(tag):
            pass
        elif Regex.w_word_match.match(tag):
            pass
        elif Regex.determiner_match.match(tag):
            model.set_quantifier(word, tag)
        #special case
        elif Regex.rp_match.match(tag):
            self.__logic_model.append(compliment.compliment())
            model = self.__logic_model[len(self.__logic_model) - 1]
            model.set_word(word, tag)

    #############################################
    # APPEND LOGIC OBJECT
    # -------------------------------------------
    # To avoid unecessary words or null pointers
    # to be added, regular expressions are used
    # to filter the words we care about
    #
    # tag: string
    def __append_logic_object(self, tag):
        if Regex.noun_phrase_match.match(tag):
            self.__logic_model.append(clause.Clause())
        elif Regex.verb_phrase_match.match(tag):
            self.__logic_model.append(predicate.Predicate())
        elif Regex.adjective_phrase_match.match(tag):
            self.__logic_model.append(compliment.compliment())
        elif Regex.prepositoinal_phrase_match.match(tag):
            self.__logic_model.append(predicate.Predicate())
        elif Regex.adverb_phrase_match.match(tag):
            self.__logic_model.append(predicate.Predicate())


if __name__ == "__main__":
    t = Tree()
    t.build("My rent is eight hundred dollars a month", draw= True)
    lst = t.get_logic_model()
    for e in lst:
        print(e)