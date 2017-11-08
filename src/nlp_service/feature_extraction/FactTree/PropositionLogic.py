from feature_extraction.FactTree import WordStack, LogicParser
from feature_extraction.Models import clause, predicate, compliment
from feature_extraction.Models import proposition


class Proposition():
    #####################################
    # CONSTRUCTOR
    def __init__(self):
        self.__proposition_lst = []
        self.__stack = WordStack.Stack()
        self.__predicates = LogicParser.Tree()

    #####################################
    # RESET
    def __reset(self):
        self.__proposition_lst = []
        self.__stack.clear()

    #############################################
    # BUILD
    # -------------------------------------------
    # Parses sentence into logical objects
    # clause / predicates
    # From the list of logical objects, make
    # correlation between them
    #
    # sentence: string
    # draw: boolean
    def build(self, sentence, draw=False):
        self.__reset()
        self.__predicates.build(sentence, draw)
        predicate_lst = self.__predicates.get_logic_model()
        self.__create_logic(predicate_lst)

    #############################################
    # CREATE LOGIC
    # -------------------------------------------
    # Will perform correct operation depending on
    # logical object type
    # clause, predicate, or compliment
    #
    # logic_lst: list
    def __create_logic(self, logic_lst):
        for i in range(len(logic_lst)):
            if isinstance(logic_lst[i], clause.Clause):
                self.__clause_operation(logic_lst[i], logic_lst, i)
            elif isinstance(logic_lst[i], predicate.Predicate):
                self.__predicate_operation(logic_lst[i], logic_lst, i)
            elif isinstance(logic_lst[i], compliment.Compliment):
                self.__compliment_operation(logic_lst[i], logic_lst, i)

    #############################################
    # CLAUSE OPERATION
    # -------------------------------------------
    # 1- If no predicate then append to clause list
    # 2- If predicate before and after the word then
    #    create relationship and append word to clause stack
    # 3- else append to compliment stack
    # 4- if last word in the list then extract features
    #
    # logic: Model.AbstractModel
    # logic_lst: list[Model.AbstractMode]
    # index: integer
    def __clause_operation(self, logic, logic_lst, index):
        if self.__stack.peek_predicate() is None:
            self.__stack.clause_stack.append(logic)

        elif isinstance(self.__stack.next(logic_lst, index), predicate.Predicate):
            if isinstance(self.__stack.previous(logic_lst, index), predicate.Predicate):
                self.__stack.compliment_stack.append(logic)
            self.__extract_relations()
            self.__stack.clause_stack.append(logic)
            return

        else:
            self.__stack.compliment_stack.append(logic)

        if self.__stack.next(logic_lst, index) is None:
            self.__extract_relations()

    #############################################
    # PREDICATE OPERATION
    # -------------------------------------------
    # 1- if no predicate in stack then append predicate
    # 2- else pop predicate and merge them into 1 phrase
    #    append new predicate
    # 3- if last word in list then extract features
    #
    # logic: Model.AbstractModel
    # logic_lst: list[Model.AbstractMode]
    # index: integer
    def __predicate_operation(self, logic_model, logic_lst, index):
        if self.__stack.peek_predicate() is None:
            self.__stack.predicate_stack.append(logic_model)

        else:
            model = self.__stack.predicate_stack.pop()
            model.merge(logic_model)
            self.__stack.predicate_stack.append(model)

        if self.__stack.next(logic_lst, index) is None:
            self.__extract_relations()

    #############################################
    # COMPLIMENT OPERATION
    # -------------------------------------------
    # 1- if last word in list then extract features
    # 2- if word in between 2 predicates then extract
    #    features and append word to clause
    # 3- else append to compliment stack
    #
    # logic: Model.AbstractModel
    # logic_lst: list[Model.AbstractMode]
    # index: integer
    def __compliment_operation(self, logic, logic_lst, index):
        if self.__stack.next(logic_lst, index) is None:
            self.__stack.compliment_stack.append(logic)
            self.__extract_relations()

        elif isinstance(self.__stack.next(logic_lst, index), predicate.Predicate):
            if isinstance(self.__stack.previous(logic_lst, index), predicate.Predicate):
                self.__stack.compliment_stack.append(logic)
            self.__extract_relations()
            self.__stack.clause_stack.append(logic)

        else:
            self.__stack.compliment_stack.append(logic)

    #############################################
    # EXTRACT RELATIONS
    # -------------------------------------------
    # 1- Pop predicate
    # 2- For ever clause map them to their compliments
    # 3- clear stack
    def __extract_relations(self):
        try:
            p = self.__stack.predicate_stack.pop()
        except IndexError:
            return
        if len(self.__stack.compliment_stack) == 0:
            self.__extract_double(predicate)
        else:
            self.__extract_triplet(p)

    #############################################
    # EXTRACT DOUBLE
    # -------------------------------------------
    # If a clause has a predicate without a
    # compliment
    #
    # predicate: tuple(word, tag)
    def __extract_double(self, p):
        for c in self.__stack.clause_stack:
            model = proposition.PropositionModel()
            model.clause = c
            model.predicate = p
            self.__proposition_lst.append(model)
        self.__stack.clear()

    #############################################
    # EXTRACT TRIPLET
    # -------------------------------------------
    # If a clause has a predicate with a compliment
    #
    # predicate: tuple(word, tag)
    def __extract_triplet(self, p):
        for c in self.__stack.clause_stack:
            for cmp in self.__stack.compliment_stack:
                model = proposition.PropositionModel()
                model.clause = c
                model.predicate = p
                model.compliment = cmp
                self.__proposition_lst.append(model)
        self.__stack.clear()

    #############################################
    # GET PROPOSITION LIST
    def get_proposition_lst(self):
        return self.__proposition_lst.copy()


if __name__ == "__main__":
    p = Proposition()
    p.build("the months remaining on my lease is 4", False)
    lst = p.get_proposition_lst()
    for e in lst:
        print(e)
        print()
