# Machine Learning Service

## 0. Table of Contents
1. [Overview](#overview)
2. [Data](#data)
3. [Installation Instruction](#installation)
4. [File Structure](#file-structure)
5. [ML API](#api)
6. [Command Line](#command-line)

## 1. Overview <a name="overview"></a>
The machine learning service is responsible for predicting the outcomes of a user's case.

Outcomes can either be categorized as either being True/False or by a numerical value. Whether a given outcome is boolean or integer is evaluated by a human and then given to the system beforehand (See section 1.6). Therefore, this sub-system makes use of both classifiers and regressors to make predictions. The inputs for both the classifier the and regressor are the facts obtained by the user's inputs. An array of outcomes is then returned.


### 1.1 Data Representation
The input and output data are all represented numerically despite having the potential to be boolean values. Below illustrates how values are treated:

0 --> False / Null
1 --> True
(n > 1) --> True AND Numerical


Numerical Values consist of:
- Dates / Time (in months)
- Money (in $)


### 1.2 Facts / Input
The inputs are stored in a numpy array consisting of only integers with the possible values listed in section 1.1. Every index of the array represents a different fact/input data point which will be used by the machine learning. The indexes of the facts are determined once the precedents are tagged (they are subject to change orders upon re-tagging the data). An input array will look as such:

[fact_1, fact_2, ..., fact_n]


Here is an example to retrieve the labels for each column:
```
from feature_extraction.post_processing.regex.regex_tagger import TagPrecedents

indexes = TagPrecedents().get_intent_index()

# print sample of the content
for i in index['outcomes_vector'][:3]:
    print(i)
```

- output:
```
(0, 'additional_indemnity_money', 'bool')
(1, 'declares_resiliation_is_correct', 'bool')
(2, 'landlord_serious_prejudice', 'bool')
```

- structure for 'indexes' variable:
```
{
    'outcomes_vector': [
        (array_index, column_label, column_type),
        (array_index, column_label, column_type)
    ],
    'facts_vector': [
        (array_index, column_label, column_type),
        (array_index, column_label, column_type)
    ]
}
```


### 1.3 outcomes / output
Similarly to section 1.2, the output will be an array of integers of the size of all the number of outcomes supported by the system. Please refer to section 1.1 for other inquiries.


### 1.4 Classification
A multiclassifier is used to predict all outcomes. In the background, SkLearn uses a different estimator per outcome in order to perform this task. When obtaining a prediction, **ALL** outcomes are either classified as True or False. Even the numerical outcomes are classified as such. If an outcome is expected to be a numerical value **AND** that outcome is True then the input is passed to the appropriate regressor in order to predict the outcome's integer value. If the previous condition isn't met then no further data manipulation is necessary for a given outcome and the classifier's prediction is simply returned for this column.

**Adding a new classifier**
New classifiers will be automatically trained upon adding regexes. See section 1.6.


### 1.5 Regression
The regressors are **only** used if the classifier predicted an outcome as True. The reason for this implementation is because the regressors are trained on bias data where we know the outcome was True. Therefore the input data must also be biased towards the same end goal.


During training, **only for regression**, the average values of every fact of the data set is obtained. The vector will look as such:

[average_column_1, average_column_2, ..., average_column_n]


This vector is kept in binary format and can be retrieved this way:
```
from util.file import Load
mean_facts_vector = Load.load_binary('model_metrics.bin')['regressor'][<name of the regressor>]['mean_facts_vector']
```

**Regression fine tuning**
When making a regressive prediction, the user's input is entered as an array of numerical values as in section 1.2.

1. Wherever a 0 is encountered in the user's input, we replace it with the average value of it's column.The purpose of this strategy is to predict more accurate results when the regressor is used. When a prediction is performed with missing input we then replace that missing input with it's average value to get a better fit on the curve.

2. During training, outliers in the dataset are removed. Outliers are determined by:
```
abs(outcome - average_of_outcomes) > (2 * std_of_outcomes)
```


**Adding a new regressor**
The regressor's estimators are crafted manually as opposed to using the SkLearn's wrapper as in section 1.4. Because the regressors require much more discreet attention, this approach was necessary. A custom wrapper is instead written, and every new regressor can inherit the AbstractRegressor Class.

1. Code new regressor (inherit abstract_regressor.py)
2. Update multi_output_regression.py to accomodate new class


### 1.6 Adding new columns (input/output)
Adding new columns is fairly simply. In the _feature_extraction/post_processing/regex/regex_lib.py_ file simply append your regex to the _regex_facts_ or _regex_outcomes_ list. The syntax is the following:

```
regex_facts = [
    (
        <column_label>, [
            re.compile(<regex_1>, re.IGNORECASE),
            re.compile(<regex_2>, re.IGNORECASE),
            re.compile(<regex_n>, re.IGNORECASE)
        ],
        <data_type>),
    ),
    (
        <column_label>, [
            re.compile(<regex_1>, re.IGNORECASE),
            re.compile(<regex_2>, re.IGNORECASE),
            re.compile(<regex_n>, re.IGNORECASE)
        ],
        <data_type>),
    ),
]
```

Type as many regular expressions as needed to cover all the dataset. Upon tagging the data a percentage of lines tagged will be displayed.

_Note: <data_type> are the following strings:_
1. "BOOLEAN"
2. "MONEY"
3. "DATE"


The newly added columns in the _regex_lib.py_ file will then automatically be used the next time the machine learning performs its training **on the condition that the data has be re-post-processed**. Be sure to create a regressor if you want to predict "DATE" or "MONEY" though (See section 1.5).


## 2. DATA <a name="data"></a>
All persistent machine learning data are stored as binaries. In order to centralize this information it is advised to upload the models on a server. These models may then be fetched in the _init.py_ script in the source directory (do not confuse with _\_\_init\_\_.py_ script). Simply append your download link to the __binary_urls__ list found in this file.

### 2.1 Accessing binary data
To load any binary files, first make sure it is stored in the _binary/data/_ folder. This should be performed automatically by the _init.py_. Then simply use the following:
```
from util.file import Load

Load.load_binary(<binary_file_name>)

```

### 2.2 Saving binary data
To save a binary file use the following:
```
from util.file import Save

Save().save_binary(<desired_binary_file_name>, model)
```

The output directory will be _binary/data/_ by default.


### 2.3 Global Variables
Some global variables are listed in _util/constant.py_


### 2.4 Binary file content
**classifier_labels.bin**
```
{
   outcome_index_0 <int>: (
       column_label <str>,
       column_type <str>
   ),
   outcome_index_n <int>: (
       column_label <str>,
       column_type <str>
   ),
}
```
**model_metrics.bin**
```
{
    'data_set':{
        'size': <int>
    },
    'classifier':{
        classifier_name_0 <str>: {
            'prediction_accuracy': <float>
        },
        classifier_name_n <str>: {
            'prediction_accuracy': <float>
        }
    },
    'regressor':{
        regressor_name_0 <str> :{
            'std': <float>,
            'variance': <float>,
            'mean_facts_vector': <numpy.array>
        },
        regressor_name_n <str> :{
            'std': <float>,
            'variance': <float>,
            'mean_facts_vector': <numpy.array>
        }
    }
```
**multi_class_svm_model.bin**
Used to predict classifier results
```
from util.file import Load
from sklearn.preprocessing import binarize

model = Load.load_binary("multi_class_svm_model.bin")
classifier_labels = Load.load_binary('classifier_labels.bin')
input_vector = [fact_1, fact_2, fact_n, ...]
data = binarize([input_vector], threshold=0)
prediction = model.predict(data)
```

**precedent_vectors.bin**
```
{
    <precedent_id> <str>:{
        'outcomes_vector': numpy.array,
        'facts_vector': numpy.array,
        'file_number': <str>,
        'name': AZ-********.txt <str>
    }
}
```
**similarity_case_numbers.bin**
An array of all case numbers. This is used to map the indices (returned by the similarity model) to case numbers

```
[
    'AZ-XXXXXX',
    'AZ-XXXXXX',
    'AZ-XXXXXX',
    'AZ-XXXXXX'
    ...
]

```


**similarity_model.bin**

Case similarity comparator. Uses NearestNeighbour algorithm. Set to return the 5 nearest neighbours.

Input: A vector, which is the concatenation of the vector containing facts and the vector containing outcomes
Output: The indices (which have a direct mapping to case numbers using similarity_case_numbers [see above]) of the 5 most similar cases

```
from util.file import Load

model = Load.load_binary("similarity_model.bin")

facts_vector = [fact_1, fact_2, fact_n, ...]
outcomes_vector = [outcome_1, outcome_2, outcome_n, ...]
input_vector = facts_vector + outcomes_vector

model.kneighbors(input_vector)
```

**\*_scaler.bin**
Every machine learning model requires a scaler to transform the data into values which will exponentially increase training time.


**\*_regressor.bin**
Models used to predict regressive results
```
from util.file import Load
from keras.models import load_model
import os

file_path = os.path.join(Path.binary_directory, '<regressor_name>')
regressor = load_model(file_path)
scaler = Load.load_binary('<your_scaler>')
model = AbstractRegressor._create_pipeline(scaler, regressor)
input_data = [fact_1, fact_2, ..., fact_n]
prediction = model.predict([input_data])
```

## 3. Installation Instructions <a name="installation"></a>

1. Add Cyberjustice Lab username as environment variables: <code>export CJL_USER={USERNAME}</code> either to your .bashrc or run it as a command
2. Add Cyberjustice Lab password as environment variables: <code>export CJL_PASS={PASSWORD}</code> either to your .bashrc or run it as a command
3. Run <code>pip3 install -r requirements.txt</code>
4. Run <code>pip3 install -r requirements_test.txt</code>

### 4. File Structure <a name="file-structure"></a>

```

----| data <all data input and output>
--------| raw
------------| text_bk <extract precedents here>

--------| binary <all saved binarized model/data>
--------| cache <temp files>
--------| test <used for unit testing>

----| feature_extraction <all data manipulation before supervised training>
--------| feature_extraction.py <driver for feature extraction (using 3 drivers above)>
--------| pre_processing
------------| pre_processing_driver
----------------| filter_precedent
--------------------| precedent_directory_cleaner.py
--------| post_processing
------------| post_processing_driver.py <driver for post_processing>
----------------| regex
--------------------| regex_entity_extraction.py
--------------------| regex_lib.py
--------------------| regex_tagger.py

----| model_learning <supervised training>
------------| classifier
----------------| classifier_dirver.py
----------------| multi_output
--------------------| multi_class_svm.py
------------| regression
----------------| regression_driver.py
----------------| single_output_regression
--------------------| abtract_regressor.py
--------------------| tenant_pays_landlord.py
--------------------| additional_indemnity.py
----------------| multi_output
--------------------| multi_output_regression.py
------------| similar_finder
----------------| similar_finder.py

----| util <common tool>
------------| log.py <logging tool>
------------| file.py <file save and load>
------------| constant.py <global variables>

----| web
--------| ml_controller.py

init.py
main.py <driver for the pipeline (feature extraction + model training>

```

## 5. ML API <a name="api"></a>

### 5.1 Predict Outcome

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
##### Success Response

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

##### Error Response

**Code** : `400 Bad Request` - *Inputs not provided*

**Code** : `404 Not Found` - *Conversation doesn"t exist*

### 5.2 Get Fact Weights

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

### 5.3 Get Anti Facts

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

### 5.4 Get Machine Learning Statistics

Get the ml stats

Used to obtain:
1) Size of data set
2) Variance of regression outcomes
3) Standard deviation of regression outcomes
4) Mean of regression outcomes
5) Prediction accuracy of each classifier

**URL**: `/statistics`

**Method**: `GET`

**Data constraints**

None

#### Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "classifier": {
        "additional_indemnity_money": {
            "prediction_accuracy": 79.8400199975003
        },
        "authorize_landlord_retake_apartment": {
            "prediction_accuracy": 99.48756405449319
        },
        "declares_housing_inhabitable": {
            "prediction_accuracy": 99.95000624921884
        },
        "declares_resiliation_is_correct": {
            "prediction_accuracy": 91.83852018497687
        },
        "landlord_prejudice_justified": {
            "prediction_accuracy": 81.07736532933383
        },
        "landlord_retakes_apartment_indemnity": {
            "prediction_accuracy": 99.72503437070367
        },
        "landlord_serious_prejudice": {
            "prediction_accuracy": 96.35045619297588
        },
        "orders_expulsion": {
            "prediction_accuracy": 91.55105611798525
        },
        "orders_immediate_execution": {
            "prediction_accuracy": 84.32695913010873
        },
        "orders_landlord_notify_tenant_when_habitable": {
            "prediction_accuracy": 100
        },
        "orders_resiliation": {
            "prediction_accuracy": 93.48831396075491
        },
        "orders_tenant_pay_first_of_month": {
            "prediction_accuracy": 98.05024371953506
        },
        "tenant_ordered_to_pay_landlord": {
            "prediction_accuracy": 83.82702162229721
        },
        "tenant_ordered_to_pay_landlord_legal_fees": {
            "prediction_accuracy": 90.32620922384702
        }
    },
    "data_set": {
        "size": 40003
    },
    "regressor": {
        "additional_indemnity_money": {
            "mean": 1477.7728467101024,
            "std": 1927.8147997893939,
            "variance": 3716469.9022870203
        },
        "tenant_pays_landlord": {
            "mean": 2148.867088064977,
            "std": 2129.510243010276,
            "variance": 4534813.8750856845
        }
    }
}
```

## 6. Using the Command Line <a name="command-line"></a>
_\* denotes optional arguments_


From the source directory _JusticeAi/src/ml_service/_ you may run:


1. Pre Processing
python main.py -pre [number of files | empty for all]
2. Post Processing
i. Each fact and outcome is listed with their number of occurences
ii. % of tagged lines is displayed
iii. python3 main.py -post [number of files | empty for all]
3. Training
\*\*_Note: Always train **svm** before the **sf** and the **svr**_
Testing results are displayed:
i. classifier: accuracy, F1, precision, recall
ii. regression: absolute error, r2
**arguments**:
    i. --svm: classifier
    ii. --svr: regressor
    iii. --sf: similarity finder
    iv. --all: classifier, regressor, similarity finder
python3 main.py -train [data size | empty for all] --svm* --sf* --svr* --all*
