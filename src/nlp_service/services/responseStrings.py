import random


class Responses:

    # Respond that a particular claim category is not implemented yet
    unimplemented_category_error = [
        "Unfortunately, I cannot help with these types of issues right now."
    ]

    # Acknowledge claim category resolution
    category_acknowledge = [
        "I see, you're having issues with {claim_category}. {first_question}",
        "As I understand it, your problems have to do with {claim_category}. {first_question}",
        "Oh yes, I see you're having problems with {claim_category}. {first_question}"
    ]

    # Asking for clarification
    clarify = [
        "I'm sorry, I can't understand what you mean. Could you please clarify? {previous_question}",
        "I didn't understand that, could you please clarify? {previous_question}",
        "I'm afraid I don't understand. Could you please rephrase? {previous_question}"
    ]

    # Giving a prediction
    prediction = {
        "LEASE_TERMINATION": {
            "success": ["I have determined that it is likely that the lease will be terminated."],
            "fail": ["I have determined that it is unlikely that the lease will be terminated."]
        },

        "missing_category": ["Sorry, I cannot yet make a prediction for this claim category."]
    }

    # Fact Questions
    fact_questions = {
        "apartment_impropre":
            [
                "Would you deem the apartment unfit for habitation?"
            ],
        "apartment_infestation":
            [
                "Is your apartment infested with any sort of pest?"
            ],
        "bothers_others":
            [
                "Have you received any complaints of the tenant acting in a disruptive manner?",
                "Has the tenant's behaviour been disruptive?"
            ],
        "disrespect_previous_judgement":
            [
                "Has the tenant failed to abide by a previous Regie judgement?"
            ],
        "landlord_inspector_fees":
            [
                "Have you at any point hired an inspector to track down the fleeing tenant?"
            ],
        "landlord_notifies_tenant_retake_apartment":
            [
                "Did you notify your tenant in advance about your intentions to retake the apartment?"
            ],
        "landlord_relocation_indemnity_fees":
            [
                "Have moving expenses been compensated when the apartment was deemed inhabitable?"
            ],
        "landlord_rent_change":
            [
                "Has there been an attempt to change the rent during the term of the lease?"
            ],
        "landlord_rent_change_doc_renseignements":
            [
                "Are there any supporting documents justifying an increase in rent?"
            ],
        "landlord_retakes_apartment":
            [
                "Is the apartment being taken back to lodge the landlord or their family member?"
            ],
        "landlord_retakes_apartment_indemnity":
            [
                "Have moving expenses been compensated when the apartment was to be retaken by the landlord?"
            ],
        "landlord_sends_demand_regie_logement":
            [
                "Has an inquiry been made with the Regie du logement?"
            ],
        "proof_of_late":
            [
                "Has a debt acknowledgment been signed by the tenant?"
            ],
        "proof_of_revenu":
            [
                "Has proof of ability to pay for the rented property been provided?"
            ],
        "rent_increased":
            [
                "Has the rent been increased during the term of the lease?"
            ],
        "tenant_bad_payment_habits":
            [
                "Has the tenant continually been late with their rent payments?"
            ],
        "tenant_continuous_late_payment":
            [
                "Does the tenant often pay their rent after it’s due?",
            ],
        "tenant_damaged_rental":
            [
                "Was there any damage done to the rented property?"
            ],
        "tenant_dead":
            [
                "Is the tenant dead?"
            ],
        "tenant_declare_insalubre":
            [
                "Is the apartment dirty?"
            ],
        "tenant_financial_problem":
            [
                "Are there any financial issues preventing the payment of rent?"
            ],
        "tenant_group_responsability":
            [
                "If there are multiple tenants inside of the apartment, do they all share the same lease?"
            ],
        "tenant_individual_responsability":
            [
                "If there are multiple tenants inside of the apartment, does each possess their own lease?"
            ],
        "tenant_landlord_agreement":
            [
                "Was there a mutually beneficial agreement set by both parties?"
            ],
        "tenant_lease_fixed":
            [
                "Is there a specified end date to the lease?"
            ],
        "tenant_left_without_paying":
            [
                "Has the tenant left the apartment?",
                "Has the tenant abandoned the apartment?"
            ],
        "tenant_monthly_payment":
            [
                "Is there a monthly rent payment?"
            ],
        "tenant_negligence":
            [
                "Has the tenant displayed any negligence with the rental?"
            ],
        "tenant_not_request_cancel_lease":
            [
                "Has a request for cancellation of the lease been given by any of the parties?"
            ],
        "tenant_owes_rent":
            [
                "Does the tenant owe rent?",
                "Does the tenant currently owe you an overdue rent payment?"
            ],
        "tenant_refuses_retake_apartment":
            [
                "Has the tenant refused the takeover of the apartment?"
            ],
        "tenant_rent_not_paid_more_3_weeks":
            [
                "Has the tenant not paid rent for over 3 weeks?",
                "Has rent not been paid by the tenant for over 3 weeks?"
            ],
        "tenant_violence":
            [
                "Has the tenant demonstrated violent behavior?",
                "Has the tenant ever been violent?"
            ],
        "tenant_withold_rent_without_permission":
            [
                "Is the tenant withholding rent without having received permission from the Regie du logement?"
            ],
        "missing_response":
            [
                "Oops, something went wrong finding a response. Sorry about that."
            ]
    }

    """
    Gets a question to ask for a particular fact
    fact_key: The fact's key
    :returns A question to ask to attempt to resolve the fact value
    """

    @staticmethod
    def fact_question(fact_key):
        if fact_key in Responses.fact_questions:
            return Responses.chooseFrom(Responses.fact_questions[fact_key])

        return Responses.chooseFrom(Responses.fact_questions["missing_response"])

    """
    Gets a statement for a prediction for a particular claim
    claim_category: The text value of the claim category
    is_success: Whether or not the judgement is 1 or 0 (from ml)
    """

    @staticmethod
    def prediction_statement(claim_category_value, is_success):
        if claim_category_value in Responses.prediction:
            if is_success:
                return Responses.chooseFrom(Responses.prediction[claim_category_value]['success'])
            else:
                return Responses.chooseFrom(Responses.prediction[claim_category_value]['fail'])

        return Responses.chooseFrom(Responses.prediction["missing_category"])

    """
    Chooses a random string from a list of strings
    string: list of strings
    :returns A random string from the list
    """

    @staticmethod
    def chooseFrom(strings):
        choice = random.choice
        return choice(strings)
