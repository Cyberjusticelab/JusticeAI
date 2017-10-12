from src.fact_extraction.Models import clause, compliment, predicate
import re


'''
LOGIC MODEL
---------------------------------------------
Contains clauses, predicates and compliments
'''


class LogicModel:
    def __init__(self):
        self.clause = clause.Clause()
        self.predicate = predicate.Predicate()
        self.compliment = compliment.compliment()
        self.previous = None
        self.next = None

    def __str__(self):
        return str(self.clause) + "\n" + str(self.predicate) + "\n" + str(self.compliment)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        elif self.clause != other.clause:
            return False
        elif self.predicate != other.predicate:
            return False
        elif self.compliment != other.compliment:
            return False
        return True

    def category_match(self, category):
        if self.compliment.category_match(category):
            return True
        elif self.predicate.category_match(category):
            return True
        elif self.clause.category_match(category):
            return True
        return False

    def get_element_from_tag(self, tag):
        tag_lst = []
        a = self.clause.get_element_from_tag(tag)
        if a is not None:
            tag_lst += a

        a = self.predicate.get_element_from_tag(tag)
        if a is not None:
            tag_lst += a

        a = self.compliment.get_element_from_tag(tag)
        if a is not None:
            tag_lst += a
        return tag_lst

    def __ne__(self, other):
        return not(self.__eq__(other))

if __name__ == '__main__':
    l1 = LogicModel()
    c1 = clause.Clause()
    c1.set_word("dwdw")
    l1.clause = c1
    l2 = LogicModel()
    c2 = clause.Clause()
    c2.set_word("dwdw")
    l2.clause = c2
    print(l1 == l2)