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