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
            "orders_resiliation": {
                True: ["I have determined that it is likely that the lease will be terminated."],
                False: ["I have determined that it is unlikely that the lease will be terminated."]
            }
        },
        "NONPAYMENT": {
            "tenant_ordered_to_pay_landlord": {
                True: ["I have determined that the tenant will likely have to pay the landlord ${} in late rent."],
                False: ["I have determined that the tenant will likely not owe any late rent payments to the landlord."]
            },
            "tenant_ordered_to_pay_landlord_legal_fees": {
                True: ["In terms of legal fees, the tenant will likely owe ${} to the landlord."],
                False: ["I don't suspect that the tenant will owe the landlord any legal fees."]
            },
            "additional_indemnity_money": {
                True: ["The tenant may owe ${} to the landlord due as compensation for prejudice."],
                False: ["It is unlikely that the tenant will owe the landlord any compensation for prejudice."]
            }
        },
        "missing_category": ["Sorry, I cannot yet make a prediction for this claim category yet."]
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
        "landlord_prejudice_justified":
            [
                ""
            ],
        "landlord_serious_prejudice":
            [
                "Has the tenant’s payment habits caused you any prejudice?"
            ],
        "tenant_continuous_late_payment":
            [
                "Has your tenant been continuously late on their rent payments?"
            ],
        "tenant_financial_problem":
            [
                "Did the tenant declare they are in a financially indisposed situation due to external factors? (i.e. job loss, injury, death in the family, etc.)"
            ],
        "tenant_owes_rent":
            [
                "Does the tenant currently owe any rent?|If so, how much do they owe?"
            ],
        "tenant_rent_not_paid_less_3_weeks":
            [
                "Has it been less than 3 weeks since the tenant has paid the landlord?"
            ],
        "tenant_rent_paid_before_hearing":
            [
                "Was the remaining balance for rent paid before the hearing?"
            ],
        "missing_response":
            [
                "Oops, something went wrong finding a response. Sorry about that."
            ]
    }

    # TODO: Text to be modified for more conversational tone
    static_claim_responses = {
        ###################
        # LANDLORD UNIQUE #
        ###################

        #################
        # TENANT UNIQUE #
        #################
        "faq_rlq_lease_cancellation_immediately_after_signing":
            {
                "TENANT":
                    [
                        "No. There is no allowable delay after signing a lease."
                    ],
            },
        "faq_rlq_landlord_neglects_necessary_repairs":
            {
                "TENANT":
                    [
                        "There are many recourses available to the tenant: rent reduction; rent deposit; authorization of the Régie to do himself the repairs; resiliation of the lease; Damages; order to force the landlord to make the repairs. A decision must be rendered by the Régie du logement allowing one of these recourses to be applied."
                    ]
            },
        "faq_likehome_landlord-harass":
            {
                "TENANT":
                    [
                        "If you are suffering harassment, find someone to possibly serve as a witness testimony and document the events with the aid of an audio-visual device (ie: cell phone).|You should file an immediate demand letter to your landlord demanding for the harassment to cease and a possible lease resiliation or compensation for moral damages.|If your landlord is not receptive, you may file at the Régie du logement for a hearing. <a href=”http://www.cdpdj.qc.ca/en/droits-de-la-personne/defendre-vos-droits/Pages/porter-plainte.aspx”>The Commission des droits de la personne et des droits de la jeunesse</a> can also give you aid.|Be aware that if you leave your dwelling, you still need to pay unless the regie or the landlord allows you to resiliate your lease."
                    ]
            },
        "faq_likehome_emergency":
            {
                "TENANT":
                    [
                        "If your landlord fails to answer the phone or does not offer help in an emergency, call a professional immediately.|If your landlord refuses to refund you for the emergency service you paid for, write a demand letter informing the landlord that you need to be compensated and file for a hearing at the Regie du logement if you are not reimbursed.|If authorities, the insurance company or the Regie du logement find that the damage to the apartment was caused by your neglect, you may face financial repercussions. If not, any financial loss during the emergency will be compensated for including temporary accommodations."
                    ]
            },
        "faq_likehome_spouse-violence":
            {
                "TENANT":
                    [
                        "If you are being abused by a spouse or a loved one, vacate the dwelling immediately and stay with friends, relatives, or contact a local shelter. File a police report immediately.|Acquire the form for <a href=”https://www.rdl.gouv.qc.ca/sites/default/files/notices/notice-of-resiliation-of-lease-because-of-spousal-violence-or-sexual-aggression_0.pdf”>requesting an attestation for lease resiliation due to spousal violence</a> and fill it out.|Bring the form to a <a href=”http://www.assermentation.justice.gouv.qc.ca/ServicesPublicsConsultation/Commissaires/Proximite/Criteres.aspx”>commissioner of oaths</a> and get it signed.|Submit the form to your <a href=”https://www.justice.gouv.qc.ca/english/recherche/district-a.asp”>local courthouse</a>.|Once you receive your attestation, you may send it with a registered letter to your landlord indicating the nature of your resiliation. Keep in mind that you must legally continue to pay rent for the dwelling until the lease is fully terminated."
                    ]
            },
        "faq_likehome_lease-transfer":
            {
                "TENANT":
                    [
                        "To transfer a lease, find a new tenant and complete the <a href=”http://lappart.info/wp-content/uploads/2015/01/Copy-of-RDL_Notice_to_assign_the_lease.pdf”>Notice to Assign the Lease</a> form.|Send this form along with a completed credit check via registered mail to your landlord.|Your landlord has 15 days to respond, and is only technically allowed to refuse for a good reason, such as the belief that the new tenant will not be able to pay rent. If the landlord does not respond in 15 days, the lease transfer is automatically approved.|Sign the <a href=”http://lappart.info/wp-content/uploads/2015/01/Copy-of-RDL_Assignment_of_the_lease_agreement.pdf”>Assignment of the Least Agreement</a> form with the new tenant that includes any conditions in transferring your lease.|If the transfer goes through, leave your copy of the original lease with the new tenant, and you’re free to move out!"
                    ]
            },
        "faq_likehome_sublet":
            {
                "TENANT":
                    [
                        "A subtenant is someone that lives in your dwelling temporarily and pays rent for the time you are gone. However, bear in mind that you are ultimately responsible for the rent and condition of the dwelling.|Once you’ve found a subtenant, pick up an official <a href=”http://legisquebec.gouv.qc.ca/en/resource/cr/R-8.1R3_EN_005_002.pdf?langCont=en&digest=FCD9136FB9F60314E31EC6F4149C94F1”>Quebec lease</a> and cross out the words “tenant” and “landlord” in the identification box and replace them with “sub-tenant” and “tenant”.|Fill out a <a href=”http://lappart.info/wp-content/uploads/2015/01/Copy-of-RDL_Notice_to_sublet_the_dwelling.pdf”>Notice to Sublet</a> form and send it to your landlord. Your landlord has 15 days to respond.|Finally, figure out a way to make rent payments with your subtenant. For example, transferring you money on a regular basis to pay the rent, or having a roommate make sure the rent gets paid."
                    ]
            },
        "faq_likehome_abandon":
            {
                "TENANT":
                    [
                        "If your dwelling becomes uninhabitable, you must first call the city inspectors to obtain an official report that deems your dwelling as unfit for habitation before abandoning it.|If your dwelling is deemed as unfit for habitation, send the <a href=”http://lappart.info/wp-content/uploads/2015/01/Copy-of-RDL_Notice_of_Abandonment.pdf”>notice of abandonement</a> form by registered mail to your landlord prior to or after abandoning the dwelling.|Bear in mind that if you are responsible for making the dwelling unfit for habitation, such as starting a fire, you must keep paying rent until your lease is resiliated.|If the reason for abandonment was out of your control, you may have the right to cease paying rent."
                    ]
            },
        "faq_likehome_landlord-contact":
            {
                "TENANT":
                    [
                        "To find your landlord’s contact information, visit <a href=”https://servicesenligne2.ville.montreal.qc.ca/sel/evalweb/index”>Consultation du rôle d'évaluation foncière</a>.|Enter the address of your dwelling. If the dwelling is found, your landlord and their contact information will be available."
                    ]
            },

        "faq_likehome_demand-letter":
            {
                "TENANT":
                    [
                        "Most of the time, informal communication with your landlord is enough to solve most problems. However, if your landlord doesn’t address the problem, you must send a demand letter.|A demand letter must be sent via registered mail. You may request this service at a post office as it requires a signature from the recipient upon delivery.|Begin the letter with the phrase “Without Prejudice” as this letter is intended as a formal notice of discontent. Bear in mind that this letter can be used as evidence in court, so refrain for foul language or personal attacks.|In your letter, include in chronological order the events, people, or places that are implicated in your demand. Provide details such as emails, phone calls, or text messages exchanged between you and the opposing party.|Once you’ve outlined your situation, make demands in point form so that the other party knows clearly what you want. Provide a time limit in which the other party must act.|Finally, inform the other party of the possible legal recourse you will take, such as taking your landlord to the Régie du Logement or taking a roommate to Civil Court, or contacting city inspectors."
                    ]
            },
        "faq_likehome_housing-committee":
            {
                "TENANT":
                    [
                        "Housing committees help walk you through your housing rights and responsibilities.|Consult <a href=”http://likehome.info/non-classe-en/finding-a-housing-committee/”>this list</a> to find one near you|For any matter that involves legal information, you will need to visit the housing committee in person."
                    ]
            },

        ##########
        # COMMON #
        ##########
        "faq_rlq_attending_hearing":
            {
                "TENANT":
                    [
                        "I must obtain a postponement of the hearing to a later date and for that I must obtain the written consent of the other party and file it at the Régie. If I cannot obtain that consent, I can send a mandatary who will ask for the postponement or I can write to the Régie du logement and ask for the postponement of the case. The reasons for the asked postponement must be indicated. It would be well advised to remit a copy of that letter to the other party. Except in the case where I have the consent of the other party, the commissioner must decide if he accepts or rejects the asked postponement."
                    ],
                "LANDLORD":
                    [
                        "I must obtain a postponement of the hearing to a later date and for that I must obtain the written consent of the other party and file it at the Régie. If I cannot obtain that consent, I can send a mandatary who will ask for the postponement or I can write to the Régie du logement and ask for the postponement of the case. The reasons for the asked postponement must be indicated. It would be well advised to remit a copy of that letter to the other party. Except in the case where I have the consent of the other party, the commissioner must decide if he accepts or rejects the asked postponement."
                    ]
            },
        "faq_rlq_abandoned_premises":
            {
                "TENANT":
                    [
                        "The landlord may attempt to minimize the damages by trying to rent the dwelling to another person.|They may claim from the tenant who has abandoned the premises a relocation indemnity to recover the lost rent.|The landlord has three years to file the application at the Régie du logement."
                    ],
                "LANDLORD":
                    [
                        "You should minimize the damages of abandonment by trying to rent the dwelling to another person.|You may claim from the tenant who has abandoned the premises a relocation indemnity to recover the lost rent.| You have three years to file the application at the Régie du logement."
                    ]
            },
        "faq_rlq_tenant_urgent_repair_costs_deducted":
            {
                "TENANT":
                    [
                        "He cannot do so without the authorization of the Régie du logement except in the case of a necessary and urgent repair and also in that case the tenant is not able to reach the landlord in order to inform him about the situation."
                    ],
                "LANDLORD":
                    [
                        "He cannot do so without the authorization of the Régie du logement except in the case of a necessary and urgent repair and also in that case the tenant is not able to reach the landlord in order to inform him about the situation."
                    ]
            },
        "faq_rlq_noisy_tenant":
            {
                "TENANT":
                    [
                        "Whatever the time of day, according to reasonable circumstances, another tenant (or you) cannot make excessive noise.|However, if the source of the noise is produced by a tenant or a party that is not on your landlord’s jurisdiction, it is out of their hands."
                    ],
                "LANDLORD":
                    [
                        "Whatever the time of day, according to reasonable circumstances, a tenant cannot make excessive noise.|However, if the source of the noise is produced by a tenant or a party that is not on your property, it is out of your hands."
                    ]
            },
        "faq_rlq_paying_repairs_for_sink_toilet":
            {
                "TENANT":
                    [
                        "The landlord must pay for the repairs except if they can successfully establish that you are responsible for the problem.|If you are able to prove that you are not responsible for the damages, if the repair is urgent (i.e. no running water), you may take the matter into your own hands and you have the right to be reimbursed or deduct the reasonable expenses from the rent."
                    ],
                "LANDLORD":
                    [
                        "You must pay for the repairs except if you can successfully prove that your tenant is responsible for the problem.|If the tenant is able to prove that they are not responsible for the damages, or if the repair is urgent (i.e. no running water), the tenant may take the matter into their own hands and have the right to be reimbursed or deduct the reasonable expenses from the rent."
                    ]
            },
        "faq_rlq_landlord_entering_occupied_apartment":
            {
                "TENANT":
                    [
                        "Your landlord must give you a 24 hour notice prior to entering your dwelling.|They must make the visit between 9:00 AM and 9:00 PM."
                    ],
                "LANDLORD":
                    [
                        "You must give your tenant a 24 hour notice prior to entering their dwelling.|You must make the visit between 9:00 AM and 9:00 PM."
                    ]
            },
        "faq_rlq_apartment_too_cold":
            {
                "TENANT":
                    [
                        "There is no specified date for heating the dwelling.|The landlord must start to heat the dwellings of the building as soon as the climatic conditions justify it.|Although neither law or most municipal by-law are specific in this area, the temperature of the dwelling should be around 21C."
                    ],
                "LANDLORD":
                    [
                        "There is no specified date for heating the dwelling.|You must start to heat the dwellings of the building as soon as the climatic conditions justify it.|Although neither law or most municipal by-law are specific in this area, the temperature of the dwelling should be around 21C."
                    ]
            },
        "faq_rlq_unreasonable_rent_increase":
            {
                "TENANT":
                    [
                        "There is no fixed rate increase applied by the Régie du logement. Each case is treated specifically.|The Régie takes into account, in calculating the rent variation, the income of the building and the municipal and school taxes, the insurance bills, the energy costs, maintenance and service costs.|Also, it sees to apply a return on capital expenditures, if there were such expenditures, and indexes the net income of the building.|In order to give an estimate of the rent variation for a dwelling, see <a href='https://www.rdl.gouv.qc.ca/en/calculation-for-the-fixing-of-rent'>this</a>."
                    ],
                "LANDLORD":
                    [
                        "There is no set-in-stone way of calculating a rent increase and each case is treated differently.|When calculating the increase, la Régie takes into account the income of the building, the municipal and school taxes, the insurance bills, the energy costs, maintenance and service costs.|Also, it sees to apply a return on capital expenditures such as maintenance or infrastructure upgrades.|In order to get an estimate of the rent increase of a lease, see <a href='https://www.rdl.gouv.qc.ca/en/calculation-for-the-fixing-of-rent'>this</a>."
                    ]
            },
        "faq_likehome_deposit-request":
            {
                "TENANT":
                    [
                        "Any key deposits, rent advances, damage deposits, security deposits, etc. are illegal and you are not obliged to pay any of them.|Consider all other requested fees (laundry machine access, pools, kitchen appliances), if already granted in your lease, as illegal too.|Lease transfer fees and sublet fees are also illegal.|However, according to the Civil Code of Quebec (article 1904), your landlord may ask for the first month’s rent to be paid in advance right after the signature of the lease.|Good news though! Even if you signed a document saying you’d pay for any of these fees, they are without effect! You cannot sign away your rights."
                    ],
                "LANDLORD":
                    [
                        "Any key deposits, rent advances, damage deposits, security deposits, etc. are illegal and tenants are not obliged to pay any of them.|Consider all other requested fees (laundry machine access, pools, kitchen appliances), if already granted in their lease, as illegal too.|Lease transfer fees and sublet fees are also illegal.|However, according to the Civil Code of Quebec (article 1904), you may ask for their first month’s rent to be paid in advance right after the signature of the lease.| Even if the tenant signed a document saying they’d pay for any of these fees, they are without effect! They cannot sign away their rights."
                    ]
            },
        "faq_likehome_personal-info":
            {
                "TENANT":
                    [
                        "Your landlord is not legally allowed to collect personal information such as copies of your study permit, driver’s license, passports, health cards, bank account numbers or even your social insurance number (SIN).|If you’ve given this kind of sensitive information to your landlord, you can:|1. Demand a copy of every piece of sensitive information in a written demand letter sent by registered mail.|2. Demand in a second letter the destruction of said information.|If the landlord doesn’t abide in full to your demand, file a claim with the Commission d'accès à l’information du Québec (CAIQ).| Even if you signed a clause saying you’ll willingly give this information away, you cannot sign away your rights, making that clause legally invalid."
                    ],
                "LANDLORD":
                    [
                        "Careful, as a landlord you are not legally allowed to collect personal information such as copies of your tenant’s study permit, driver licenses, passports, health cards, bank account numbers or even their social insurance number (SIN).|Your tenant is legally allowed to file a claim with the Commission d'accès à l’information du Québec (CAIQ) if you request such information.|Even if the tenant signed a clause saying they willingly gave this information away, they cannot sign away their rights, making that clause legally invalid."
                    ]
            },

        "faq_likehome_rl31":
            {
                "TENANT":
                    [
                        "The RL-31 allows you to claim your housing as part of the solidarity tax credit.|You are eligible to receive the RL-31 if you are a tenant or a subtenant.|Your landlord is responsible for providing you with the RL-31 prior to the last day of February.|If your landlord has not provided you with your RL-31, contact them and ask them to provide one as it is required by law.|If they refuse to do so, call Revenu Québec and they will accept a copy of your lease."
                    ],

                "LANDLORD":
                    [
                        "The RL-31 allows your tenant to claim the provided housing as part of the solidarity tax credit.|Tenants and subtenants are equally eligible to receive it.|You are responsible by law for providing them with the RL-31 prior to the last day of February."
                    ]
            },
        "faq_likehome_negligence":
            {
                "TENANT":
                    [
                        "If you are sure that you were not negligent and damage was caused due to wear and tear|write your landlord a demand letter stating that something is broken and needs fixing."
                    ],
                "LANDLORD":
                    [
                        "If you are sure that the tenant was negligent and damage was not caused due to wear and tear|present your arguments in front of la Régie du logement if the tenant refuses to pay for the damages."
                    ]
            },
        "faq_likehome_credit-check":
            {
                "TENANT":
                    [
                        "The easiest way to obtain a credit check is to go online.|Find a reputable credit score provider online (which typically costs you a small fee) and provide them with your SIN.| Your credit report will then immediately be available to print out and submit to your landlord."
                    ],
                "LANDLORD":
                    [
                        "The responsibility of providing a credit report is your tenant’s.|The easiest way to obtain a credit check for your tenant is for them to get it online.|They need to find a reputable credit score provider online (which typically costs them a small fee) and provide them with their SIN.|Their credit report will then immediately be available to print out and submit to you."
                    ]
            },

        #########
        # ERROR #
        #########
        "missing_response":
            [
                "Sorry, I'm unable to help you with that at the moment."
            ]
    }

    @staticmethod
    def fact_question(fact_key):
        """
        Gets a question to ask for a particular fact
        :param fact_key: The fact's key as a string
        :return:A question to ask to attempt to resolve the fact value
        """

        if fact_key in Responses.fact_questions:
            return Responses.chooseFrom(Responses.fact_questions[fact_key])

        return Responses.chooseFrom(Responses.fact_questions["missing_response"])

    @staticmethod
    def faq_statement(claim_category_value, person_type):
        """
        Gets the answer to a faq key, may be context sensitive based on person_type
        :param claim_category_value: The string value of the claim category
        :param person_type: The string value of the person type
        :return: The answer to a FAQ question
        """

        if person_type not in Responses.static_claim_responses[claim_category_value]:
            return Responses.chooseFrom(Responses.static_claim_responses["missing_response"])

        return Responses.chooseFrom(Responses.static_claim_responses[claim_category_value][person_type])

    @staticmethod
    def prediction_statement(claim_category_value, prediction_dict):
        """
        Gets a statement for a prediction for a particular claim
        :param claim_category_value: The string value of the claim category
        :param prediction_dict: A dict of prediction keys from the ML service
        :return: A string of predictions based on determined outcomes
        """

        # Check if dict is empty
        if not bool(prediction_dict) or claim_category_value not in Responses.prediction:
            return Responses.chooseFrom(Responses.prediction["missing_category"])

        all_predictions = []
        for prediction in prediction_dict:
            prediction_value = prediction_dict[prediction]
            prediction_predicate = int(prediction_value) > 0
            prediction_text = Responses.chooseFrom(
                Responses.prediction[claim_category_value][prediction][prediction_predicate]).format(prediction_value)
            all_predictions.append(prediction_text)

        return "|".join(all_predictions)

    @staticmethod
    def chooseFrom(strings):
        """
        Chooses a random string from a list of strings
        :param strings: List of strings
        :return: A random string from the list
        """
        choice = random.choice
        return choice(strings)
