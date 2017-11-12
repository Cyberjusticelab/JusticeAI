import random


class Responses:
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
