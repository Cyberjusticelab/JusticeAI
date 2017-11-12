import random


class StaticStrings:
    # Asking for Acceptance to legal conditions
    disclaimer = [
        "Hello {name}! Before we start, I want to make it clear that I am not a replacement for a lawyer and any information I provide you with is not meant to be construed as legal advice. Always check in with your legal professional. You can read more about our terms of use <a href='/legal' target='_blank'>here</a>. Do you accept these conditions?"
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

    @staticmethod
    def chooseFrom(strings):
        choice = random.choice
        return choice(strings)
