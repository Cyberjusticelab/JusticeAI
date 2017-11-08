import unittest

from feature_extraction.FactTree import LogicParser
from feature_extraction.Models import clause, predicate, compliment


class TestLogicParser(unittest.TestCase):
    def test_build_word_order(self):
        parser = LogicParser.Tree()
        parser.build("My lease expires on the 31st of October.", False)
        word_lst = parser.get_logic_model()
        self.assertEqual(type(word_lst[0]), clause.Clause)
        self.assertEqual(type(word_lst[1]), predicate.Predicate)
        self.assertEqual(type(word_lst[2]), predicate.Predicate)
        self.assertEqual(type(word_lst[3]), clause.Clause)
        self.assertEqual(type(word_lst[4]), predicate.Predicate)
        self.assertEqual(type(word_lst[5]), clause.Clause)

        parser.build("The dog was blue", False)
        word_lst = parser.get_logic_model()
        self.assertEqual(type(word_lst[0]), clause.Clause)
        self.assertEqual(type(word_lst[1]), predicate.Predicate)
        self.assertEqual(type(word_lst[2]), compliment.Compliment)
