from src.fact_extraction.FactTree import LogicParser, WordStack
from src.fact_extraction.Models import logic, clause, predicate, compliment


class Proposition():
    #####################################
    # CONSTRUCTOR
    def __init__(self):
        self.proposition_lst = []
        self.stack = WordStack.Stack()

    #####################################
    # RESET
    def __reset(self):
        self.proposition_lst = []
        self.stack.clear()

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
    def build(self, sentence, draw = False):
        self.__reset()
        predicates = LogicParser.Tree()
        predicates.build(sentence, draw)
        predicate_lst = predicates.get_logic_model()
        self.create_logic(predicate_lst)

    #############################################
    # CREATE LOGIC
    # -------------------------------------------
    # Will perform correct operation depending on
    # logical object type
    # clause, predicate, or compliment
    #
    # logic_lst: list
    def create_logic(self, logic_lst):
        for i in range(len(logic_lst)):
            if logic_lst[i].get_word() is None:
                continue
            elif type(logic_lst[i]) == clause.Clause:
                self.clause_operation(logic_lst[i], logic_lst, i)
            elif type(logic_lst[i]) == predicate.Predicate:
                self.predicate_operation(logic_lst[i], logic_lst, i)
            elif type(logic_lst[i]) == compliment.compliment:
                self.compliment_operation(logic_lst[i], logic_lst, i)

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
    def clause_operation(self, logic, logic_lst, index):
        if self.stack.peek_predicate() is None:
            self.stack.clause_stack.append(logic)

        elif type(self.stack.next(logic_lst, index)) == predicate.Predicate:
            if type(self.stack.previous(logic_lst, index)) == predicate.Predicate:
                self.stack.compliment_stack.append(logic)
            self.extract_relations()
            self.stack.clause_stack.append(logic)
            return

        else:
            self.stack.compliment_stack.append(logic)

        if self.stack.next(logic_lst, index) is None:
            self.extract_relations()

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
    def predicate_operation(self, logic_model, logic_lst, index):
        if self.stack.peek_predicate() is None:
            self.stack.predicate_stack.append(logic_model)

        else:
            model = self.stack.predicate_stack.pop()
            model.set_word(logic_model.get_word())
            self.stack.predicate_stack.append(model)

        if self.stack.next(logic_lst, index) is None:
            self.extract_relations()

    #############################################
    # COMPLIMENT OPERATION
    # -------------------------------------------
    # 1- if last word in list then extract features
    # 2- if word in between 2 predicates then extract
    #    features and append word to clause --> not sure about this one
    # 3- else append to compliment stack
    #
    # logic: Model.AbstractModel
    # logic_lst: list[Model.AbstractMode]
    # index: integer
    def compliment_operation(self, logic, logic_lst, index):
        if self.stack.next(logic_lst, index) is None:
            self.stack.compliment_stack.append(logic)
            self.extract_relations()

        elif type(self.stack.next(logic_lst, index)) == predicate.Predicate:
            if type(self.stack.previous(logic_lst, index)) == predicate.Predicate:
                self.stack.compliment_stack.append(logic)
            self.extract_relations()
            self.stack.clause_stack.append(logic)

        else:
            self.stack.compliment_stack.append(logic)

    #############################################
    # EXTRACT RELATIONS
    # -------------------------------------------
    # 1- Pop predicate
    # 2- For ever clause map them to their compliments
    # 3- clear stack
    def extract_relations(self):
        predicate = self.stack.predicate_stack.pop()
        for clause in self.stack.clause_stack:
            for compliment in self.stack.compliment_stack:
                model = logic.LogicModel()
                model.clause = clause
                model.predicate = predicate
                model.compliment = compliment
                self.proposition_lst.append(model)
        self.stack.clear()

    def get_proposition_lst(self):
        return self.proposition_lst.copy()


if __name__ == "__main__":
    p = Proposition()
    p.build("The cat was happy and the dog was sad", True)
    lst = p.get_proposition_lst()
    for e in lst:
        print(e)
        print()