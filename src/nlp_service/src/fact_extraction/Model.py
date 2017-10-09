from src.fact_extraction import clause, predicate, compliment


class Logic_Model:
    def __init__(self):
        self.clause = clause.Clause()
        self.predicate = predicate.Predicate()
        self.compliment = compliment.compliment()

    def __str__(self):
        return str(self.clause) + "\n" + str(self.predicate) + "\n" + str(self.compliment)