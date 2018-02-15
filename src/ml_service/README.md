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
      "orders_resiliation" : 1,
      ...
    },
    "similar_precedents" : [
    	{
    		"precedent": "AZ-1111111",
    		"distance": 1.23123
    	},
    	{
    		"precedent": "AZ-2222222",
    		"distance": 1.23123
    	},
    	{
    		"precedent": "AZ-3333333",
    		"distance": 1.23123
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
        "not_important_facts": [
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
