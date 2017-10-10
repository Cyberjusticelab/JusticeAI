import uuid


class Claim(object):
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.person = None
        self.facts = []
        self.questions = []
        self.answers = []

    def set_person(self, person):
        self.person = person

    def add_question(self, question):
        self.questions.append(question)

    def add_answer(self, answer):
        self.answers.append(answer)
