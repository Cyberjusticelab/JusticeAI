import uuid


'''class Question(object):
    def __init__(self):
        self.answers = []

    def get_answers(self):
        return self.answers

    def add_answer(self, answer):
        self.answers.extend(answer)'''


class Conversation(object):
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.person = None
        self.facts = []
        self.questions = []
        self.answers = []
        self.counter = 0

    def delete_last_set(self):
        self.counter -= 1
        del self.questions[-1]
        del self.answers[-1]
        del self.facts[-1]

    def get_set(self, row):
        return "Question: "+self.questions[row]+"/n Answer: "+self.answers[row]+"/n Fact: "+self.facts[row]+". /n END."

    def get_counter(self):
        return self.counter

    def get_name(self):
        return self.name

    def get_person(self):
        return self.person

    def get_facts(self):
        return self.facts

    def get_id(self):
        return self.id

    def get_specific_fact(self, row):
        return self.facts[row]

    def get_specific_question(self, row):
        return self.questions[row]

    def get_specific_answer(self, row):
        return self.answers[row]

    def get_questions(self):
        return self.questions

    def get_answers(self):
        return self.answers

    def set_person(self, person):
        self.person = person

    def set_name__(self, name):
        self.name = name

    def add_fact(self, fact):
        self.facts.extend(fact)
        self.counter += 1

    def add_question(self, question):
        self.questions.extend(question)

    def add_answer(self, answer):
        self.answers.extend(answer)

