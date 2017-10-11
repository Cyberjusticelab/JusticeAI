import random


class RandomStringList:
    def __init__(self):
        self.strings = []

    def pick(self):
        choice = random.choice
        return choice(self.strings)


class WelcomeStrings(RandomStringList):
    def __init__(self):
        super().__init__()
        self.strings = [
            "Hello {name}! Are you a landlord or a tenant?",
            "Hey {name}, I'm here to help you with your rental disputes! Are you a landlord or a tenant?",
            "Nice to meet you {name}, are you a landlord or a tenant?"
        ]