import random


class Responses:
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

    # Acknowledge claim category resolution
    category_acknowledge = [
        "I see, you're having issues with {claim_category}. {first_question}",
        "As I understand it, your problems have to do with {claim_category}. {first_question}",
        "Oh yes, I know all about problems with {claim_category}. {first_question}"
    ]

    # Asking for clarification
    clarify = [
        "I'm sorry, I can't understand what you mean. Could you please clarify?",
        "I didn't understand that, could you please clarify?",
        "I'm afraid I dont understand. Could you please rephrase?"
    ]

    # Fact Questions
    fact_questions = {
        "lease_type": ["Is there a specified end date to your lease?"],
        "has_lease_expired": ["Has the lease expired already?"],
        "is_student": ["Are you a student?"],
        "is_habitable": ["How would you describe your dwelling? Is it habitable?"],
        "is_rent_in_lease": ["Is the rent specified in the lease?"],
        "rent_in_lease_amount": ["What is the amount of the rent"],
        "in_default": ["How long has it been since you haven't paid rent?"],
        "over_three_weeks": ["Has payment not been made in over three weeks?"],
        "has_abandoned": ["Have you seen your tenant?"],
        "is_rent_advance": ["Has the rent been asked to be paid in advance?"],
        "first_month_rent_paid": ["Is it only for the first month?"],

        "missing_response": ["Oops, something went wrong finding a response. Sorry about that."]
    }

    @staticmethod
    def fact_question(fact_key):
        if fact_key in Responses.fact_questions:
            return Responses.chooseFrom(Responses.fact_questions[fact_key])

        return Responses.chooseFrom(Responses.fact_questions["missing_response"])

    @staticmethod
    def chooseFrom(strings):
        choice = random.choice
        return choice(strings)
