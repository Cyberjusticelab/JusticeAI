# Machine Learning Service

## Installation Instructions

1. Add Cyberjustice Lab username as environment variables: <code>export CJL_USER={USERNAME}</code> either to your .bashrc or run it as a command
2. Add Cyberjustice Lab password as environment variables: <code>export CJL_PASS={PASSWORD}</code> either to your .bashrc or run it as a command
3. Run <code>pip install -r requirements.txt</code>
4. Run <code>pip install -r requirements_test.txt</code>



## Extract Facts from Data

1. Download the precedent data
2. Extract the zip to the root directory (e.g. JusticeAI/text_bk)
3. Run <code>python feature_extraction/fact_clustering/main.py</code>



## ML API

### Predict Outcome

Predict the outcome based on given facts and demands. Returns an array of predicted outcomes.

**URL** : `/predict`

**Method** : `POST`

**Data constraints**

Provide facts_vector and demands_vector, with key values for each fact/demand.

```json
{
  "demands" : {
    "demand_lease_modification": 1,
    "demand_resiliation": 1,
    "landlord_claim_interest_damage": 0,
    "landlord_demand_access_rental": 1,
    "landlord_demand_bank_fee": 1,
    "landlord_demand_damage": 1,
    "landlord_demand_legal_fees": 1,
    "landlord_demand_retake_apartment": 1,
    "landlord_demand_utility_fee": 1,
    "landlord_fix_rent": 1,
    "landlord_lease_termination": 1,
    "landlord_money_cover_rent": 1,
    "paid_judicial_fees": 1,
    "tenant_claims_harassment": 0,
    "tenant_cover_rent": 1,
    "tenant_demands_decision_retraction": 1,
    "tenant_demand_indemnity_Code_Civil": 1,
    "tenant_demand_indemnity_damage": 1,
    "tenant_demand_indemnity_judicial_fee": 1,
    "tenant_demand_interest_damage": 1,
    "tenant_demands_money": 1,
    "tenant_demand_rent_decrease": 1,
    "tenant_respect_of_contract": 1,
    "tenant_eviction": 0
  },
  "facts" : {
    "absent" : 1,
    "apartment_impropre" : 0,
    "apartment_infestation" : 1,
    "asker_is_landlord" : 1,
    "asker_is_tenant" : 1,
    "bothers_others" : 1,
    "disrespect_previous_judgement" : 1,
    "incorrect_facts" : 1,
    "landlord_inspector_fees" : 1,
    "landlord_notifies_tenant_retake_apartment" : 1,
    "landlord_pays_indemnity" : 1,
    "landlord_prejudice_justified" : 1,
    "landlord_relocation_indemnity_fees" : 1,
    "landlord_rent_change" : 1,
    "landlord_rent_change_doc_renseignements" : 1,
    "landlord_rent_change_piece_justification" : 1,
    "landlord_rent_change_receipts" : 0,
    "landlord_retakes_apartment" : 1,
    "landlord_retakes_apartment_indemnity" : 1,
    "landlord_sends_demand_regie_logement" : 0,
    "landlord_serious_prejudice" : 1,
    "lease" : 1,
    "proof_of_late" : 1,
    "proof_of_revenu" : 0,
    "rent_increased" : 1,
    "tenant_bad_payment_habits" : 1,
    "tenant_continuous_late_payment" : 1,
    "tenant_damaged_rental" : 1,
    "tenant_dead" : 1,
    "tenant_declare_insalubre" : 1,
    "tenant_financial_problem" : 0,
    "tenant_group_responsability" : 1,
    "tenant_individual_responsability" : 1,
    "tenant_is_bothered" : 1,
    "lack_of_proof" : 1,
    "tenant_landlord_agreement" : 0,
    "tenant_lease_fixed" : 1,
    "tenant_lease_indeterminate" : 1,
    "tenant_left_without_paying" : 0,
    "tenant_monthly_payment" : 1,
    "tenant_negligence" : 1,
    "tenant_not_request_cancel_lease" : 1,
    "tenant_owes_rent" : 1,
    "tenant_refuses_retake_apartment" : 1,
    "tenant_rent_not_paid_less_3_weeks" : 1,
    "tenant_rent_not_paid_more_3_weeks" : 0,
    "tenant_rent_paid_before_hearing" : 1,
    "tenant_violence" : 1,
    "tenant_withold_rent_without_permission" : 1,
    "violent" : 1
  }
}
```
#### Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "outcomes_vector": {
      "lease_resiliation" : 1
    }
}
```

#### Error Response

**Code** : `400 Bad Request` - *Inputs not provided*

**Code** : `404 Not Found` - *Conversation doesn't exist*

---


## Run Tests and Lints

```
export COMPOSE_FILE=ci
./cjl up -d && ./cjl run ml_service
```

## Using Azure
1 - cd JusticeAi
2- python3 -m src.ml_service.feature_extraction.main <command>
3- The <command> list is as follows (a '/' indicates an 'or'):

    i) --dbscan -facts/decisions min_sample_size epsilon
       example: --dbscan -facts 10 0.3

    ii) --hdbscan -facts/decisions min_cluster_size min_sample_size
       example: --hdbscan -decisions 20 5

    iii) k-means ** still needs refactoring

    iv) --parse -facts/decision
       example: --parse -facts
       ** this command generates the preprocessing models needed for the clustering

4- The preprocessing models need to be moved to JusticeAi/src/ml_service/ml_models/
   The reason they are not automatically moved is to prevent the risk of overwriting
   a previously better model

5- All outputs will be sotred in JusticeAi/src/ml_service/output/*
   cd to this directory to view, get, move them

6- Running the algorithm will overrite any existing files for that particular
   algorithm in the output folder.
        (running hdbscan twice consecutively will destroy the first run's results)
        (running k-means followed by hdbscan won't destroy results -- they are saved in seperate folders)

   **If you run DBSCAN then please clear JusticeAi/src/ml_service/output/dbscan_cluster_dir/
     The algorithm will overrite files, however if cluster size is lesser than the
     previous run then you will not overrite ALL files and you will end up with more text files than actual clusters.
     The binary model however will always be the most up to date.

7- Outputs are saved as text files and as binary models. The text files represent
   the clusters while the binary file is the model itself.

