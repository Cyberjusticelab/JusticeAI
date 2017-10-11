from src.fact_extraction.Models import clause, compliment, predicate


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