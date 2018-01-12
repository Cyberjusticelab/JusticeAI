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

    # TODO: Text to be modified for more conversational tone
    static_claim_responses = {
        "FAQ_RLQ_attending_hearing": "I must obtain a postponement of the hearing to a later date and for that I must obtain the written consent of the other party and file it at the Régie. If I cannot obtain that consent, I can send a mandatary who will ask for the postponement or I can write to the Régie du logement and ask for the postponement of the case. The reasons for the asked postponement must be indicated. It would be well advised to remit a copy of that letter to the other party. Except in the case where I have the consent of the other party, the commissioner must decide if he accepts or rejects the asked postponement.",
        "FAQ_RLQ_abandoned_premises": "The landlord must minimize the damages by trying to rent the dwelling to another person. He may claim the tenant who has abandoned the premises a relocation indemnity to recover the lost rent. The landlord has three years to file the application at the Régie du logement.",
        "FAQ_RLQ_lease_cancellation_immediately_after_signing": "No. There is no allowable delay after signing a lease.",
        "FAQ_RLQ_leave_apartment_no_lease": "A tenant always has a lease, whether it is written or verbal. If there is no fixed term for the lease, the tenant must give to the landlord a notice of one month before leaving the premises.",
        "FAQ_RLQ_leave_apartment_no_lease": "A tenant always has a lease, whether it is written or verbal. If there is no fixed term for the lease, the tenant must give to the landlord a notice of one month before leaving the premises.",
        "FAQ_RLQ_tenant_urgent_repair_costs_deducted": "He cannot do so without the authorization of the Régie du logement except in the case of a necessary and urgent repair and also in that case the tenant is not able to reach the landlord in order to inform him about the situation.",
        "FAQ_RLQ_landlord_neglects_necessary_repairs": "There are many recourses available to the tenant: rent reduction; rent deposit; authorization of the Régie to do himself the repairs; resiliation of the lease; Damages; order to force the landlord to make the repairs. A decision must be rendered by the Régie du logement allowing one of these recourses to be applied.",
        "FAQ_RLQ_noisy_tenant": "Whatever the time of day, according to reasonable circumstances, a tenant cannot make excessive noise.",
        "FAQ_RLQ_paying_repairs_for_sink_toilet": "The landlord must pay for the repairs except if they can establish that the tenant is responsible for the problem.",
        "FAQ_RLQ_landlord_entering_occupied_apartment": "The landlord must give the tenant a 24 hour notice and make the visit between 9:00 AM and 9:00 PM.",
        "FAQ_RLQ_apartment_too_cold": "There is no specified date for heating the apartment. The landlord must start to heat the dwellings of the building as soon as the climatic conditions justify it. Although neither law or most municipal by-law are specific in this area, the temperature of the dwelling should be around 21C",
        "FAQ_RLQ_unreasonable_rent_increase": "There is no fixed rate increase applied by the Régie du logement. Each case is treated specifically. The Régie takes into account, in calculating the rent variation, the income of the building and the municipal and school taxes, the insurance bills, the energy costs, maintenance and service costs. Also, it sees to apply a return on capital expenditures, if there were such expenditures, and indexes the net income of the building. In order to calculate precisely the rent variation for a dwelling, see the section: https:\/\/www.rdl.gouv.qc.ca\/en\/calculation-for-the-fixing-of-rent"
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
