from src.fact_extraction.FactTree.PropositionLogic import Proposition
from src.fact_extraction.WordToInteger.word_to_int import WordToInt
import re


class Answer():
    query_dict = {
        "lease_term_length": {
            "topic": ['lease', 'time'],
            "fact": ('NN', 'time'),
            "return": ('CD', int)
        },
        "lease_ends_in": {
            "topic": ['lease', 'time'],
            "fact": ('NN', 'time'),
            "return":('CD', int)
        },
        "rent_in_lease_amount": {
            "topic": ['pay'],
            "return": ('CD', int)
        }
    }

    def __init__(self):
        self.propositions = Proposition()

    def query(self, query, sentence):
        answer_type = self.query_dict[query.lower()]
        self.propositions.build(sentence)
        proposition_lst = self.propositions.get_proposition_lst()
        return self.find_relevance(proposition_lst, answer_type)

    def find_relevance(self, proposition_lst, answer_type):
        topics = answer_type['topic'].copy()
        return_type = answer_type['return']
        topics_found = 0
        initial_topic_len = len(topics)
        possible_answers = []

        for propositions in proposition_lst:
            possible_answers += propositions.get_element_from_tag(return_type[0])
            for i in range(len(topics) - 1, -1, -1):
                if propositions.category_match(topics[i]):
                    topics.pop()
                    topics_found += 1

        if topics_found == 0:
            return "Off topic"
        elif topics_found < initial_topic_len:
            return "Insufficient data"
        else:
            return self.extract_answer(possible_answers, answer_type)

    def extract_answer(self, answer_lst, answer_type):
        fact = answer_type['fact']
        for answers in answer_lst:
            if answers.get_category() == fact[1]:
                return self.parse_answer(answers, answer_type)
        return "On topic but missing information"

    def parse_answer(self, answer, answer_type):
        words = answer.get_word()
        regex = re.compile(answer_type['return'][0])
        value = ""
        for word in words:
            if regex.match(word[1]):
                value += word[0]

        try:            
            return int(value)
        except:
            model = WordToInt()
            return model.text2int(value)

if __name__ == '__main__':
    a = Answer()
    result = a.query("lease_term_length", "I have 3 dogs and my lease is twenty months")
    print(result)
    result = a.query("lease_term_length", "my lease expires in 4 years")
    print(result)
    result = a.query("lease_term_length", "my lease is time")
    print(result)
