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
        "I'm sorry, I can't understand what you mean. Could you please clarify? {previous_question}",
        "I didn't understand that, could you please clarify? {previous_question}",
        "I'm afraid I don't understand. Could you please rephrase? {previous_question}"
    ]

    # Fact Questions
    fact_questions = {
        "absent":
            [
                ""
            ],
        "apartment_impropre":
            [
                ""
            ],
        "apartment_infestation":
            [
                "Is your apartment infested with any sort of pest?"
            ],
        "asker_is_landlord":
            [
                ""
            ],
        "asker_is_tenant":
            [
                ""
            ],
        "bothers_others":
            [
                ""
            ],
        "disrespect_previous_judgement":
            [
                ""
            ],
        "incorrect_facts":
            [
                ""
            ],
        "landlord_inspector_fees":
            [
                "Have you at any point hired an inspector to track down the fleeing tenant?"
            ],
        "landlord_notifies_tenant_retake_apartment":
            [
                "Did you notify your tenant in advance about your intentions to "
            ],
        "landlord_pays_indemnity":
            [
                ""
            ],
        "landlord_prejudice_justified":
            [
                ""
            ],
        "landlord_relocation_indemnity_fees":
            [
                ""
            ],
        "landlord_rent_change":
            [
                ""
            ],
        "landlord_rent_change_doc_renseignements":
            [
                ""
            ],
        "landlord_rent_change_piece_justification":
            [
                ""
            ],
        "landlord_rent_change_receipts":
            [
                ""
            ],
        "landlord_retakes_apartment":
            [
                ""
            ],
        "landlord_retakes_apartment_indemnity":
            [
                ""
            ],
        "landlord_sends_demand_regie_logement":
            [
                ""
            ],
        "landlord_serious_prejudice":
            [
                ""
            ],
        "lease":
            [
                ""
            ],
        "proof_of_late":
            [
                ""
            ],
        "proof_of_revenu":
            [
                ""
            ],
        "rent_increased":
            [
                ""
            ],
        "tenant_bad_payment_habits":
            [
                ""
            ],
        "tenant_continuous_late_payment":
            [
                "Does the tenant often pay their rent after it’s due?",
                "Is the tenant often paying their rent late?",
                "Has the tenant continually been late with their rent payments?"
            ],
        "tenant_damaged_rental":
            [
                ""
            ],
        "tenant_dead":
            [
                ""
            ],
        "tenant_declare_insalubre":
            [
                ""
            ],
        "tenant_financial_problem":
            [
                ""
            ],
        "tenant_group_responsability":
            [
                ""
            ],
        "tenant_individual_responsability":
            [
                ""
            ],
        "tenant_is_bothered":
            [
                ""
            ],
        "lack_of_proof":
            [
                ""
            ],
        "tenant_landlord_agreement":
            [
                ""
            ],
        "tenant_lease_fixed":
            [
                ""
            ],
        "tenant_lease_indeterminate":
            [
                ""
            ],
        "tenant_left_without_paying":
            [
                "Has the tenant left the apartment?",
                "Has the tenant abandoned the apartment?"
            ],
        "tenant_monthly_payment":
            [
                ""
            ],
        "tenant_negligence":
            [
                ""
            ],
        "tenant_not_request_cancel_lease":
            [
                ""
            ],
        "tenant_owes_rent":
            [
                ""
            ],
        "tenant_refuses_retake_apartment":
            [
                ""
            ],
        "tenant_rent_not_paid_less_3_weeks":
            [
                ""
            ],
        "tenant_rent_not_paid_more_3_weeks":
            [
                ""
            ],
        "tenant_rent_paid_before_hearing":
            [
                ""
            ],
        "tenant_violence":
            [
                ""
            ],
        "tenant_withold_rent_without_permission":
            [
                ""
            ],
        "violent":
            [
                ""
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
    Chooses a random string from a list of strings
    string: list of strings
    :returns A random string from the list
    """

    @staticmethod
    def chooseFrom(strings):
        choice = random.choice
        return choice(strings)
