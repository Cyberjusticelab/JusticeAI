import random


class StaticStrings:
    # Asking for Acceptance to legal conditions
    disclaimer = [
        "Hello {name}! Before we start, I want to make it clear that I am not a replacement for a lawyer and any information I provide you with is not meant to be construed as legal advice. Always check in with your legal professional. You can read more about our terms of use <a href='/legal'>here</a>. Do you accept these conditions?"
    ]

    # Asking for person type
    welcome = [
        "Hello {name}! To start off, are you a landlord or a tenant?",
        "Hey {name}, I'm here to help you with your rental disputes! Are you a landlord or a tenant?",
        "Nice to meet you {name}, are you a landlord or a tenant?",
        "You've got questions, I've got answers! Are you a landlord or a tenant, {name}?"
    ]

    # Asking for initial problem description
    problem_inquiry_landlord = [
        "So {name}, I see you're a landlord. What issue can I help you with today?",
        "What kind of issue are you having as a landlord, {name}?",
        "I can help you with all sorts of landlord issues, {name}! Describe your problem to me, let's see what we can do."
    ]

    problem_inquiry_tenant = [
        "I see you're a tenant, {name}. If you have it on hand, it would be very helpful if you could upload your lease. What issue can I help you with today?",
        "What kind of issue are you having as a tenant, {name}? Upload your lease if you have it, it might help in resolving your issues.",
        "I can help you with all sorts of tenant issues, {name}! Describe your problem to me and upload your lease if available."
    ]

    # Acknowledge claim category resolution
    category_acknowledge = [
        "I see, you're having issues with {claim_category}. {first_question}",
        "As I understand it, your problems have to do with {claim_category}. {first_question}",
        "Oh yes, I know all about problems with {claim_category}. {first_question}"
    ]

    # Asking for clarification
    clarify = [
        "I'm sorry, I can't understand what you mean.",
        "I didn't understand that, could you please clarify?",
        "Huh?"
    ]

    @staticmethod
    def chooseFrom(strings):
        choice = random.choice
        return choice(strings)
