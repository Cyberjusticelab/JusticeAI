'''
This class helps me do all the annoying
list operations
'''


class Stack:
    def __init__(self):
        self.compliment_stack = []
        self.clause_stack = []
        self.predicate_stack = []

    #####################################
    # PEEK PREDICATE
    def peek_predicate(self):
        return self.peek(self.predicate_stack)

    #####################################
    # PEEK CLAUSE
    def peek_clause(self):
        return self.peek(self.clause_stack)

    #####################################
    # PEEK COMPLIMENT
    def peek_compliment(self):
        return self.peek(self.compliment_stack)

    #####################################
    # PEEK
    def peek(self, stack):
        try:
            return stack[len(stack) - 1]
        except:
            return None

    #####################################
    # NEXT
    # -----------------------------------
    # Returns next element in the list
    #
    # lst: list
    # index: integer
    def next(self, lst, index):
        try:
            return lst[index + 1]
        except:
            return None

    #####################################
    # PREVIOUS
    # -----------------------------------
    # Returns the previous element in the list
    #
    # lst: list
    # index: integer
    def previous(self, lst, index):
        try:
            return lst[index - 1]
        except:
            return None

    #####################################
    # CLEAr
    def clear(self):
        self.compliment_stack.clear()
        self.clause_stack.clear()
        self.predicate_stack.clear()
