import re

from feature_extraction.FactTree.PropositionLogic import Proposition
from feature_extraction.WordToInteger.word_to_int import WordToInt


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
            "return": ('CD', int)
        },
        "rent_in_lease_amount": {
            "topic": ['pay'],
            "fact": ('NN', 'pay'),
            "return": ('CD', int)
        }
    }

    #########################################
    # CONSTRUCTOR
    def __init__(self):
        self.propositions = Proposition()
        self.current_dict_entry = None

    ##################################################
    # QUERY
    # ------------------------------------------------
    # Attempts to extract the answer from a user
    # based on the topic.
    #
    # query: string
    # sentence: string
    def query(self, query, sentence):
        self.current_dict_entry = self.query_dict[query.lower()]
        self.propositions.build(sentence)
        proposition_lst = self.propositions.get_proposition_lst()
        return self.__find_possible_answers(proposition_lst)

    #########################################
    # FIND POSSIBLE ANSWERS
    # ---------------------------------------
    # Finds all propositions which match
    # the category of answer we are searching for
    #
    # proposition_lst: List of all proposition statements
    def __find_possible_answers(self, proposition_lst):
        topics = self.current_dict_entry['topic'].copy()
        tag = self.current_dict_entry['return'][0]
        topics_found = 0
        initial_topic_len = len(topics)
        possible_answers = []

        for propositions in proposition_lst:
            if propositions.contains_tag(tag):
                possible_answers.append(propositions)
            for i in range(len(topics) - 1, -1, -1):
                if propositions.category_match(topics[i]):
                    topics.pop()
                    topics_found += 1

        if topics_found == 0:
            # return "Off topic"
            return None
        elif topics_found < initial_topic_len:
            # return "Insufficient old_data"
            return None
        else:
            return self.__extract_answer(possible_answers)

    #########################################
    # EXTRACT ANSWER
    # ---------------------------------------
    # Finds the proposition which is in the
    # same category as the answer we want
    # to extract
    #
    # answer: List of propositions
    def __extract_answer(self, possible_answers):
        fact = self.current_dict_entry['fact']
        tag = self.current_dict_entry['return'][0]
        for answers in possible_answers:
            if fact[1] in answers.category:
                return self.__parse_answer(answers.get_tagged_word(tag))
        # return "On topic but missing information"
        return None

    #########################################
    # PARSE ANSWER
    # ---------------------------------------
    # Get the keyword from the proposition
    # to answer the query
    #
    # answer: List of clause/predicate/compliments
    def __parse_answer(self, answer):
        regex = re.compile(self.current_dict_entry['return'][0])
        value = ""
        for word_set in answer:
            words = word_set.get_word()
            for word in words:
                if regex.match(word[1]):
                    value += word[0]
        return self.__format_answer(value)

    ##############################################
    # FORMAT ANSWER
    # --------------------------------------------
    # Formats the answer in whatever value is expected
    # Will support booleans in the future
    #
    # value: string
    def __format_answer(self, value):
        return_type = self.current_dict_entry['return'][1]
        # More types supported in the future
        if return_type == int:
            return self.__return_int(value)

    #########################################
    # RETURN INT
    # ---------------------------------------
    # Tries to convert the value to an integer
    # if it fails then parse the word and give
    # it's integer value
    # nine hundred two --> 902
    #
    # value: string
    @staticmethod
    def __return_int(value):
        try:
            return int(value)
        except ValueError:
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
    result = a.query("lease_term_length", "I have 4 Mihai and my lease ends in 2 months")
    print(result)
