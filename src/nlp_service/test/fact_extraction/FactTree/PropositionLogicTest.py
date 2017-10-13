import unittest
from feature_extraction.Models import proposition, clause, predicate, compliment
from feature_extraction.FactTree import PropositionLogic


class TestPropositionLogic(unittest.TestCase):
    @staticmethod
    def create_logic_model(c, p, cmp):
        model = proposition.PropositionModel()
        model.clause = c
        model.predicate = p
        model.compliment = cmp
        return model

    @staticmethod
    def create_clause_model(word, qualifier, quantifier):
        model = clause.Clause()
        for words in word:
            model.add_word(words[0], words[1])
        if qualifier is not None:
            for q in qualifier:
                model.add_attribute(q[0], q[1])
        if quantifier is not None:
            model.set_quantifier(quantifier[0], quantifier[1])
        return model

    @staticmethod
    def create_predicate_model(word, qualifier):
        model = predicate.Predicate()
        for words in word:
            model.add_word(words[0], words[1])
        if qualifier is not None:
            for q in qualifier:
                model.add_attribute(q[0], q[1])
        return model

    @staticmethod
    def create_compliment_model(word, qualifier, quantifier):
        model = compliment.Compliment()
        for words in word:
            model.add_word(words[0], words[1])
        if qualifier is not None:
            for q in qualifier:
                model.add_attribute(q[0], q[1])
        if quantifier is not None:
            model.set_quantifier(quantifier[0], quantifier[1])
        return model

    @staticmethod
    def equal_lists(list1, list2):
        if len(list1) != len(list2):
            return False
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return False
        return True

    def proposition_match(self, builder, sentence, model_list):
        builder.build(sentence)
        proposition_list = builder.get_proposition_lst()
        value = self.equal_lists(model_list, proposition_list)
        model_list.clear()
        return value

    def test_complex_sentences(self):
        model_lst = []
        p = PropositionLogic.Proposition()

        # ---------------------------------------------------------
        # Sentence 1
        cl = self.create_clause_model([('my', 'PRP$'), ('coffee', 'NN')], None, None)
        pr = self.create_predicate_model([("was", 'VBD')], None)
        cmp = self.create_compliment_model([("cold", 'JJ')], [('too', 'RB')], None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        cl = self.create_clause_model([("I", 'PRP')], None, None)
        pr = self.create_predicate_model([("heated", 'VBN')], None)
        cmp = self.create_clause_model([("it", 'PRP')], None, None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        cl = self.create_clause_model([("it", 'PRP')], None, None)
        pr = self.create_predicate_model([("in", 'IN')], None)
        cmp = self.create_clause_model([("microwave", 'NN')], None, ("the", 'DT'))
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        sentence = "Because my coffee was too cold, I heated it in the microwave."
        self.assertTrue(self.proposition_match(p, sentence, model_lst))

        # ---------------------------------------------------------
        # Sentence 2
        cl = self.create_clause_model("he", None, None)
        pr = self.create_predicate_model("was", None)
        cmp = self.create_compliment_model("rich", ['very'], None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        cl = self.create_clause_model("he", None, None)
        pr = self.create_predicate_model("was", ["still"])
        cmp = self.create_compliment_model("unhappy", ['very'], None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        sentence = "Though he was very rich, he was still very unhappy."
        self.assertTrue(self.proposition_match(p, sentence, model_lst))

        # ---------------------------------------------------------
        # Sentence 3
        cl = self.create_clause_model("She", None, None)
        pr = self.create_predicate_model("returned", None)
        cmp = self.create_clause_model("computer", None, "the")
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        cl = self.create_clause_model("she", None, None)
        pr = self.create_predicate_model("noticed", None)
        cmp = self.create_clause_model("it", None, None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        cl = self.create_clause_model("it", None, None)
        pr = self.create_predicate_model("was, damaged", None)
        cmp = self.create_compliment_model(None, None, None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        sentence = "She returned the computer after she noticed it was damaged."
        self.assertTrue(self.proposition_match(p, sentence, model_lst))

        # ---------------------------------------------------------
        # Sentence 4
        cl = self.create_clause_model("cost", None, 'the')
        pr = self.create_predicate_model("goes", None)
        cmp = self.create_compliment_model("up", None, None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        cl = self.create_clause_model("customers", None, None)
        pr = self.create_predicate_model("buy", None)
        cmp = self.create_clause_model("clothing", ['less'], None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        sentence = "When the cost goes up, customers buy less clothing."
        self.assertTrue(self.proposition_match(p, sentence, model_lst))

        # ---------------------------------------------------------
        # Sentence 5
        cl = self.create_clause_model("she", None, None)
        pr = self.create_predicate_model("was", None)
        cmp = self.create_compliment_model("bright, ambitious", None, None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        cl = self.create_clause_model("she", None, None)
        pr = self.create_predicate_model("became", None)
        cmp = self.create_clause_model("manager", None, None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        cl = self.create_clause_model("manager", None, None)
        pr = self.create_predicate_model("in", None)
        cmp = self.create_clause_model("time", None, "no")
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        sentence = "As she was bright and ambitious, she became manager in no time."
        self.assertTrue(self.proposition_match(p, sentence, model_lst))

        # ---------------------------------------------------------
        # Sentence 6
        cl = self.create_clause_model("you", None, None)
        pr = self.create_predicate_model("go", None)
        cmp = self.create_clause_model("you", None, None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        cl = self.create_clause_model("you", None, None)
        pr = self.create_predicate_model("find", ['always'])
        cmp = self.create_clause_model("beauty", None, None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        sentence = "Wherever you go, you can always find beauty."
        self.assertTrue(self.proposition_match(p, sentence, model_lst))

        # ---------------------------------------------------------
        # Sentence 7
        cl = self.create_clause_model("movie", ['very', 'long'], "The")
        pr = self.create_predicate_model("was", ['still'])
        cmp = self.create_compliment_model("enjoyable", ['very'], None)
        model_lst.append(self.create_logic_model(cl, pr, cmp))

        sentence = "The movie, though very long, was still very enjoyable."
        self.assertTrue(self.proposition_match(p, sentence, model_lst))
        '''        
        p.build("Evergreen trees are a symbol of fertility because they do not die in the winter.")
        p.build("The actor was happy he got a part in a movie, although the part was a small one.")
        p.build("The museum was very interesting, as I expected.")
        p.build("Because he is rich, people make allowance for his idiosyncrasies.")
        p.build("The professional, who had been thoroughly trained, was at a loss to explain.")
        p.build("When she was younger, she believed in fairy tales.")
        p.build("After the tornado hit the town, there was little left standing.")
        p.build("I have to save this coupon because I don’t have time to shop right now.")
        p.build("Let’s go back to the restaurant where we had our first date.")
        p.build("Although my cousin invited me, I chose not to go to the reunion.")
        p.build("As genes change over time, evolution progresses.")
        p.build("I really didn’t like the play although the acting was very good.")
        p.build("Everyone laughed when he got a cream pie smashed in his face.")
        p.build("After twenty years, he still had feelings for her.")
        p.build("Some people tell me that money can’t buy happiness.")
        '''
