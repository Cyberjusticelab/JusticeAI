# Machine Learning Service

## Installation Instructions

1. Add Cyberjustice Lab username as environment variables: <code>export CJL_USER={USERNAME}</code> either to your .bashrc or run it as a command
2. Add Cyberjustice Lab password as environment variables: <code>export CJL_PASS={PASSWORD}</code> either to your .bashrc or run it as a command
3. Run <code>pip install -r requirements.txt</code>
4. Run <code>pip install -r requirements_test.txt</code>

### File Structure:

```

----| data <all data input and output>
--------| raw <extract the raw data here>
--------| binary <all saved binarized model/data>
--------| cache <temp files>
--------| cluster
------------| fact
------------| decision

----| feature_extraction <all data manipulation before supervised training>
--------| clustering
------------| dbscan
------------| hdbscan
------------| k_means
------------| optimization
------------| clustering.py <driver for clustering>
--------| pre_processing
------------| precedent_model
------------| regex_parse
------------| word_vector
------------| pre_processing.py <driver for pre_processing>
------------| pre_processor.py
--------| post_processing
------------| precedent_vector
------------| post_processing.py <driver for post_processing>
--------| feature_extraction.py <driver for feature extraction (using 3 drivers above)>

----| model_learning <supervised training>
------------| neural_net
------------| model_training.py <driver for supervised training>

----| util <common tool>
------------| log.py <logging tool>
------------| file.py <file save and load>
------------| constant.py <global variables>

init.py
main.py <driver for the pipeline (feature extraction + model training>

```

## Extracting Data

- For binarized data and model, place under `data/binary`
- For precedent raw data (*.txt), place under `data/raw`
- Run `python init` to download French word vector



## ML API

### Predict Outcome

Predict the outcome based on given facts and demands. Returns an array of predicted outcomes as well as similar precedents. The precedents have distances assigned to them. The lower the distance, the more similar it is.

**URL** : `/predict`

**Method** : `POST`

**Data constraints**

Provide facts_vector and demands_vector, with key values for each fact/demand.

```json
{
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
    "additional_indemnity_money": "221",
    "authorize_landlord_retake_apartment": "0",
    "declares_housing_inhabitable": "0",
    "declares_resiliation_is_correct": "0",
    "landlord_prejudice_justified": "1",
    "landlord_retakes_apartment_indemnity": "0",
    "landlord_serious_prejudice": "0",
    "orders_expulsion": "1",
    "orders_immediate_execution": "1",
    "orders_landlord_notify_tenant_when_habitable": "0",
    "orders_resiliation": "1",
    "orders_tenant_pay_first_of_month": "0",
    "tenant_ordered_to_pay_landlord": "643",
    "tenant_ordered_to_pay_landlord_legal_fees": "80"
  },
  "probabilities_vector": {
    "additional_indemnity_money": "0.93",
    "authorize_landlord_retake_apartment": "1.0",
    "declares_housing_inhabitable": "1.0",
    "declares_resiliation_is_correct": "0.94",
    "landlord_prejudice_justified": "0.74",
    "landlord_retakes_apartment_indemnity": "1.0",
    "landlord_serious_prejudice": "1.0",
    "orders_expulsion": "0.88",
    "orders_immediate_execution": "0.72",
    "orders_landlord_notify_tenant_when_habitable": "1.0",
    "orders_resiliation": "0.91",
    "orders_tenant_pay_first_of_month": "0.99",
    "tenant_ordered_to_pay_landlord": "0.99",
    "tenant_ordered_to_pay_landlord_legal_fees": "0.91"
  },
  "similar_precedents": [
    {
      "distance": 0.3423500835013649,
      "facts": {
        "apartment_dirty": false,
        "asker_is_landlord": true,
        "asker_is_tenant": false,
        "bothers_others": false,
        "disrespect_previous_judgement": false,
        "landlord_inspector_fees": "0.0",
        "landlord_notifies_tenant_retake_apartment": false,
        "landlord_pays_indemnity": false,
        "landlord_relocation_indemnity_fees": "0.0",
        "landlord_rent_change": false,
        "landlord_rent_change_doc_renseignements": false,
        "landlord_retakes_apartment": false,
        "landlord_sends_demand_regie_logement": false,
        "rent_increased": false,
        "signed_proof_of_rent_debt": false,
        "tenant_continuous_late_payment": false,
        "tenant_damaged_rental": false,
        "tenant_dead": false,
        "tenant_financial_problem": false,
        "tenant_group_responsability": false,
        "tenant_individual_responsability": true,
        "tenant_is_bothered": false,
        "tenant_lease_indeterminate": false,
        "tenant_left_without_paying": false,
        "tenant_monthly_payment": "900.0",
        "tenant_not_paid_lease_timespan": "0.0",
        "tenant_owes_rent": "970.0",
        "tenant_refuses_retake_apartment": false,
        "tenant_rent_not_paid_more_3_weeks": true,
        "tenant_sends_demand_regie_logement": false,
        "tenant_withold_rent_without_permission": false,
        "violent": false
      },
      "outcomes": {
        "additional_indemnity_money": "70.0",
        "authorize_landlord_retake_apartment": false,
        "declares_housing_inhabitable": false,
        "declares_resiliation_is_correct": false,
        "landlord_prejudice_justified": true,
        "landlord_retakes_apartment_indemnity": false,
        "landlord_serious_prejudice": false,
        "orders_expulsion": true,
        "orders_immediate_execution": true,
        "orders_landlord_notify_tenant_when_habitable": false,
        "orders_resiliation": true,
        "orders_tenant_pay_first_of_month": false,
        "tenant_ordered_to_pay_landlord": "970.0",
        "tenant_ordered_to_pay_landlord_legal_fees": "88.0"
      },
      "precedent": "AZ-51211608"
    },
    {
      "distance": 0.3429019324281239,
      "facts": {
        "apartment_dirty": false,
        "asker_is_landlord": true,
        "asker_is_tenant": false,
        "bothers_others": false,
        "disrespect_previous_judgement": false,
        "landlord_inspector_fees": "0.0",
        "landlord_notifies_tenant_retake_apartment": false,
        "landlord_pays_indemnity": false,
        "landlord_relocation_indemnity_fees": "0.0",
        "landlord_rent_change": false,
        "landlord_rent_change_doc_renseignements": false,
        "landlord_retakes_apartment": false,
        "landlord_sends_demand_regie_logement": false,
        "rent_increased": false,
        "signed_proof_of_rent_debt": false,
        "tenant_continuous_late_payment": false,
        "tenant_damaged_rental": false,
        "tenant_dead": false,
        "tenant_financial_problem": false,
        "tenant_group_responsability": false,
        "tenant_individual_responsability": true,
        "tenant_is_bothered": false,
        "tenant_lease_indeterminate": false,
        "tenant_left_without_paying": false,
        "tenant_monthly_payment": "735.0",
        "tenant_not_paid_lease_timespan": "0.0",
        "tenant_owes_rent": "873.0",
        "tenant_refuses_retake_apartment": false,
        "tenant_rent_not_paid_more_3_weeks": true,
        "tenant_sends_demand_regie_logement": false,
        "tenant_withold_rent_without_permission": false,
        "violent": false
      },
      "outcomes": {
        "additional_indemnity_money": "0.0",
        "authorize_landlord_retake_apartment": false,
        "declares_housing_inhabitable": false,
        "declares_resiliation_is_correct": false,
        "landlord_prejudice_justified": true,
        "landlord_retakes_apartment_indemnity": false,
        "landlord_serious_prejudice": false,
        "orders_expulsion": true,
        "orders_immediate_execution": true,
        "orders_landlord_notify_tenant_when_habitable": false,
        "orders_resiliation": true,
        "orders_tenant_pay_first_of_month": false,
        "tenant_ordered_to_pay_landlord": "873.0",
        "tenant_ordered_to_pay_landlord_legal_fees": "80.0"
      },
      "precedent": "AZ-51176404"
    },
    {
      "distance": 0.49114649102172725,
      "facts": {
        "apartment_dirty": false,
        "asker_is_landlord": true,
        "asker_is_tenant": false,
        "bothers_others": false,
        "disrespect_previous_judgement": false,
        "landlord_inspector_fees": "0.0",
        "landlord_notifies_tenant_retake_apartment": false,
        "landlord_pays_indemnity": false,
        "landlord_relocation_indemnity_fees": "0.0",
        "landlord_rent_change": false,
        "landlord_rent_change_doc_renseignements": false,
        "landlord_retakes_apartment": false,
        "landlord_sends_demand_regie_logement": false,
        "rent_increased": false,
        "signed_proof_of_rent_debt": false,
        "tenant_continuous_late_payment": false,
        "tenant_damaged_rental": false,
        "tenant_dead": false,
        "tenant_financial_problem": false,
        "tenant_group_responsability": false,
        "tenant_individual_responsability": true,
        "tenant_is_bothered": false,
        "tenant_lease_indeterminate": false,
        "tenant_left_without_paying": false,
        "tenant_monthly_payment": "770.0",
        "tenant_not_paid_lease_timespan": "0.0",
        "tenant_owes_rent": "1360.0",
        "tenant_refuses_retake_apartment": false,
        "tenant_rent_not_paid_more_3_weeks": true,
        "tenant_sends_demand_regie_logement": false,
        "tenant_withold_rent_without_permission": false,
        "violent": false
      },
      "outcomes": {
        "additional_indemnity_money": "590.0",
        "authorize_landlord_retake_apartment": false,
        "declares_housing_inhabitable": false,
        "declares_resiliation_is_correct": false,
        "landlord_prejudice_justified": true,
        "landlord_retakes_apartment_indemnity": false,
        "landlord_serious_prejudice": false,
        "orders_expulsion": true,
        "orders_immediate_execution": true,
        "orders_landlord_notify_tenant_when_habitable": false,
        "orders_resiliation": true,
        "orders_tenant_pay_first_of_month": false,
        "tenant_ordered_to_pay_landlord": "1360.0",
        "tenant_ordered_to_pay_landlord_legal_fees": "81.0"
      },
      "precedent": "AZ-51212451"
    },
    {
      "distance": 0.49200755901067444,
      "facts": {
        "apartment_dirty": false,
        "asker_is_landlord": true,
        "asker_is_tenant": false,
        "bothers_others": false,
        "disrespect_previous_judgement": false,
        "landlord_inspector_fees": "0.0",
        "landlord_notifies_tenant_retake_apartment": false,
        "landlord_pays_indemnity": false,
        "landlord_relocation_indemnity_fees": "0.0",
        "landlord_rent_change": false,
        "landlord_rent_change_doc_renseignements": false,
        "landlord_retakes_apartment": false,
        "landlord_sends_demand_regie_logement": false,
        "rent_increased": false,
        "signed_proof_of_rent_debt": false,
        "tenant_continuous_late_payment": false,
        "tenant_damaged_rental": false,
        "tenant_dead": false,
        "tenant_financial_problem": false,
        "tenant_group_responsability": false,
        "tenant_individual_responsability": true,
        "tenant_is_bothered": false,
        "tenant_lease_indeterminate": false,
        "tenant_left_without_paying": false,
        "tenant_monthly_payment": "945.0",
        "tenant_not_paid_lease_timespan": "0.0",
        "tenant_owes_rent": "1290.0",
        "tenant_refuses_retake_apartment": false,
        "tenant_rent_not_paid_more_3_weeks": true,
        "tenant_sends_demand_regie_logement": false,
        "tenant_withold_rent_without_permission": false,
        "violent": false
      },
      "outcomes": {
        "additional_indemnity_money": "345.0",
        "authorize_landlord_retake_apartment": false,
        "declares_housing_inhabitable": false,
        "declares_resiliation_is_correct": false,
        "landlord_prejudice_justified": true,
        "landlord_retakes_apartment_indemnity": false,
        "landlord_serious_prejudice": false,
        "orders_expulsion": true,
        "orders_immediate_execution": true,
        "orders_landlord_notify_tenant_when_habitable": false,
        "orders_resiliation": true,
        "orders_tenant_pay_first_of_month": false,
        "tenant_ordered_to_pay_landlord": "1290.0",
        "tenant_ordered_to_pay_landlord_legal_fees": "72.0"
      },
      "precedent": "AZ-51201834"
    },
    {
      "distance": 0.4933548500076463,
      "facts": {
        "apartment_dirty": false,
        "asker_is_landlord": true,
        "asker_is_tenant": false,
        "bothers_others": false,
        "disrespect_previous_judgement": false,
        "landlord_inspector_fees": "0.0",
        "landlord_notifies_tenant_retake_apartment": false,
        "landlord_pays_indemnity": false,
        "landlord_relocation_indemnity_fees": "0.0",
        "landlord_rent_change": false,
        "landlord_rent_change_doc_renseignements": false,
        "landlord_retakes_apartment": false,
        "landlord_sends_demand_regie_logement": false,
        "rent_increased": false,
        "signed_proof_of_rent_debt": false,
        "tenant_continuous_late_payment": false,
        "tenant_damaged_rental": false,
        "tenant_dead": false,
        "tenant_financial_problem": false,
        "tenant_group_responsability": false,
        "tenant_individual_responsability": true,
        "tenant_is_bothered": false,
        "tenant_lease_indeterminate": false,
        "tenant_left_without_paying": false,
        "tenant_monthly_payment": "800.0",
        "tenant_not_paid_lease_timespan": "0.0",
        "tenant_owes_rent": "1400.0",
        "tenant_refuses_retake_apartment": false,
        "tenant_rent_not_paid_more_3_weeks": true,
        "tenant_sends_demand_regie_logement": false,
        "tenant_withold_rent_without_permission": false,
        "violent": false
      },
      "outcomes": {
        "additional_indemnity_money": "0.0",
        "authorize_landlord_retake_apartment": false,
        "declares_housing_inhabitable": false,
        "declares_resiliation_is_correct": false,
        "landlord_prejudice_justified": true,
        "landlord_retakes_apartment_indemnity": false,
        "landlord_serious_prejudice": false,
        "orders_expulsion": true,
        "orders_immediate_execution": true,
        "orders_landlord_notify_tenant_when_habitable": false,
        "orders_resiliation": true,
        "orders_tenant_pay_first_of_month": false,
        "tenant_ordered_to_pay_landlord": "0.0",
        "tenant_ordered_to_pay_landlord_legal_fees": "92.0"
      },
      "precedent": "AZ-51391660"
    }
  ]
}
```

#### Error Response

**Code** : `400 Bad Request` - *Inputs not provided*

**Code** : `404 Not Found` - *Conversation doesn"t exist*

### Get Fact Weights

Get the weights of every outcome sorted by descending order of importance

**URL**: `/weights`

**Method**: `GET`

**Data constraints**

None

#### Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "additional_indemnity_money": {
        "important_facts": [
            "asker_is_landlord",
            "tenant_withold_rent_without_permission",
            "tenant_refuses_retake_apartment",
            "tenant_monthly_payment",
            "tenant_not_paid_lease_timespan"
        ],
        "additional_facts": [
            "tenant_financial_problem",
            "tenant_owes_rent",
            "asker_is_tenant",
            "tenant_damaged_rental",
            "tenant_individual_responsability",
            "signed_proof_of_rent_debt",
            "tenant_lease_indeterminate",
            "tenant_dead",
            "tenant_is_bothered",
            "bothers_others"
        ]
    }
}
```

### Get Anti Facts

Get the anti facts

Left hand side always initialized to 1 and right hand side to 0

**URL**: `/antifacts`

**Method**: `GET`

**Data constraints**

None

#### Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "tenant_rent_not_paid_less_3_weeks": "tenant_rent_not_paid_more_3_weeks",
    "tenant_lease_fixed": "tenant_lease_indeterminate",
    "not_violent": "violent",
    "tenant_individual_responsability": "tenant_group_responsability"
}
```
---


## Run Tests and Lints

```
export COMPOSE_FILE=ci
./cjl up -d && ./cjl run ml_service
```

## Using the Command Line
* denotes optional arguments

1-  Commands

    python main.py -train [data size | empty for all] --svm* --sf* --weights* --evaluate*
    python main.py -pre [number of files | empty for all]
    python main.py -post [number of files | empty for all]

2- all binary files saved to data/binary

3- all text files to data/cluster

4- all raw_data to data/raw
