'''
This class helps me do all the annoying
list operations
'''


class Stack:
    def __init__(self):
        self.compliment_stack = []
        self.clause_stack = []
        self.predicate_stack = []

    def peek_predicate(self):
        return self.peek(self.predicate_stack)

    def peek_clause(self):
        return self.peek(self.clause_stack)

    def peek_compliment(self):
        return self.peek(self.compliment_stack)

    def peek(self, stack):
        try:
            return stack[len(stack) - 1]
        except:
            return None

    def next(self, lst, index):
        try:
            return lst[index + 1]
        except:
            return None

    def previous(self, lst, index):
        try:
            return lst[index - 1]
        except:
            return None

    def clear(self):
        self.compliment_stack.clear()
        self.clause_stack.clear()
        self.predicate_stack.clear()