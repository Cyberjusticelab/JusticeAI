import random


class RandomStringList:
    def __init__(self):
        self.strings = []

    def pick(self):
        choice = random.choice
        return choice(self.strings)


class ClarifyStrings(RandomStringList):
    def __init__(self):
        super().__init__()
        self.strings = [
            "I'm sorry, I can't understand what you mean.",
            "I didn't understand that, could you please clarify?",
            "Huh?"
        ]


class WelcomeStrings(RandomStringList):
    def __init__(self):
        super().__init__()
        self.strings = [
            "Hello {name}! To start off, are you a landlord or a tenant?",
            "Hey {name}, I'm here to help you with your rental disputes! Are you a landlord or a tenant?",
            "Nice to meet you {name}, are you a landlord or a tenant?",
            "You've got questions, I've got answers! Are you a landlord or a tenant, {name}?",
            "BEGIN QUESTIONING PROCEDURE P-001.....I mean, hi {name}! Tell me, are you a landlord or a tenant?"
        ]


class ProblemInquiryStrings(RandomStringList):
    def __init__(self):
        super().__init__()
        self.strings = [
            "So {name}, I see you're a {person_type}. What issue can I help you with today?",
            "What kind of issue are you having as a {person_type}, {name}?",
            "I can help you with all sorts of {person_type} issues, {name}! Describe your problem to me, let's see what we can do.",
            "You're a {person_type}?! Me too! Us {person_type}s need to stick together. Describe your problem to me {name}, I'm all ears.",
        ]


class CategoryInquiryStrings(RandomStringList):
    def __init__(self):
        super().__init__()
        self.strings = [
            "I see, you're having issues with {claim_category}.",
            "As I understand it, your problems have to do with {claim_category}.",
            "Oh yes, I know all about problems with {claim_category}."
        ]