from rasa.rasa_classifier import RasaClassifier
from util.parse_dataset import CreateJson

# Generate RASA training data from text files
jsonCreator = CreateJson()

# Claim Categories
jsonCreator.parse_directory("/rasa/text/category/", "/rasa/data/category/")

# Facts generated from base file
fact_names = [
    "apartment_impropre",
    "apartment_infestation",
    "bothers_others",
    "disrespect_previous_judgement",
    "landlord_inspector_fees",
    "landlord_notifies_tenant_retake_apartment",
    "landlord_relocation_indemnity_fees",
    "landlord_rent_change_doc_renseignements",
    "landlord_rent_change",
    "landlord_retakes_apartment_indemnity",
    "landlord_retakes_apartment",
    "landlord_sends_demand_regie_logement",
    "proof_of_late",
    "proof_of_revenu",
    "rent_increased",
    "tenant_bad_payment_habits",
    "tenant_damaged_rental",
    "tenant_dead",
    "tenant_declare_insalubre",
    "tenant_landlord_agreement",
    "tenant_lease_fixed",
    "tenant_monthly_payment",
    "tenant_negligence",
    "tenant_not_request_cancel_lease",
    "tenant_refuses_retake_apartment",
    "tenant_violence",
    "tenant_group_responsability",
    "tenant_individual_responsability"
]
jsonCreator.identical_fact_list("/rasa/text/fact/base/yes_no.txt", fact_names, "/rasa/data/fact/")

# Facts with their own data sets
jsonCreator.parse_directory("/rasa/text/fact/individual/", "/rasa/data/fact/")

# Generate model data for training
rasa = RasaClassifier()
rasa.train(force_train=True, initialize_interpreters=False)
