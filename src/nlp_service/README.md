# Natural Language Processing Service

## Run Tests and Lints

```
./cjl test nlp_service
```

*Warning*: Have at the very least 8GB of RAM available to run nlp_service tests.

We recommend an i5 Broadwell CPU and above if you so wish to run tests locally.

The team used atomic commits and pushes while working on Natural Language Processing to run the tests on its continuous integration tool (Travis in this case).

## Installing requirements

```
pip3 install -r requirements_test.txt
```

---
# NLP API

## Classify claim category

Extract a claim category from a user's message. Returns a question based on the claim category found, or a clarification question.

**URL** : `/claim_category`

**Method** : `POST`

**Data constraints**

Provide the conversation id and the message.

```json
{
    "conversation_id": 1,
    "message": "I am being evicted"
}
```
#### Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "message": "I see you're having problems with lease termination. Have you kept up with your rent payments?",
    "progress": 0
}
```

#### Error Response

**Code** : `400 Bad Request` - *Inputs not provided*

**Code** : `404 Not Found` - *Conversation doesn't exist*

---
## Submit message

Submits a user input to the NLP service. Returns the next question to ask, or a clarification question.

**URL** : `/submit_message`

**Method** : `POST`

**Data constraints**

Provide the conversation id and the message.

```json
{
    "conversation_id": 1,
    "message": "My rent is $900 per month."
}
```
#### Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "message": "Have you kept up with your rent payments?",
    "progress": 10
}
```

#### Error Response

**Code** : `400 Bad Request` - *Inputs not provided*

**Code** : `404 Not Found` - *Conversation doesn't exist*

---

# RASA JSON Tool
The **util.parse_dataset.py** module and the associated **CreateJson** class can be used to create json training data for RASA NLU.

#### Format
```
[meta]
() = entity_name1, entity_extractor(optional)
{} = entity_name2, entity_extractor(optional)

[regex_features]
name:regex

[entity_synonyms]
entity:synonym1, synonym2

[common_examples: intent_name1]
sentence1
sentence2

[common_examples: intent_name2]
sentence1
sentence2

```

- **[]** are reserved characters used to identify sections
- **meta** section allows for the definition of meta-characters that define entities
- **regex_features** are simply regex features
- **entity_synonyms** are simply entity synonyms
- **common_examples:intent_name** are common examples for a particular intent


#### Example
```
[meta]
() = money, ner_duckling

[regex_features]
money:$\d(.)?+|\d(.)?+$

[common_examples: true]
my landlord increased my rent by ($500)
i owe my landlord (40 dollars)

[common_examples: false]
i don't owe my landlord any money
i dont have any debts
no

```

### Command Line Use
python3 -m util.parse_dataset <read_dir> <write_dir>

#### Example
python3 -m util.parse_dataset ~/Documents/ ~/Documents/Json/

**DO NOT FORGET THE '/' AT THE END OF YOUR DIRECTORY**

## Outlier detection

*As of April 10th 2018 the outlier detection is not being used by the NLP service*

This is due to a lack of data of what is considered an "outlier answer".

## Adding a new claim category to the product

**Two kinds of claim categories:**
* Developed claim categories:
  * Series of questions that the user answers to resolve facts
  * Multiple outcomes dynamically calculated by the ml_service
  * a conclusive view with a dashboard containing resolved facts and most similar legal cases to theirs
* FAQs have:
  * one long and developed answer resumed from websites such as [Regie du logement](rdl.gouv.qc.ca), [Educaloi](https://www.educaloi.qc.ca/categories/habitation) or [LikeHome](http://likehome.info/).

1. Add the claim category to nlp_service/controllers/nlp_controller.py in "conversation.claim_category" inside of the "classify_claim_category" function
2. Define the new claim category inside of the class "ClaimCategory" in postgresql_db/models.py
3. Define the new category inside of the the *.txt file in nlp_service/rasa/text/category (depending whether or not it is a category belonging to a tenant (category_tenant.txt) or a landlord (category_landlord.txt))
     *We recommend keeping track of FAQ vs developed categories by writing "faq_AbrievationOfSource_factname"*
4. Write in nlp_service/services/response_strings.py your response if the claim you wrote is an "FAQ"
5. At this stage you should either have a complete FAQ *or* an empty developed claim category, which you'll have to add facts to! (following section)

## Adding a new fact (includes adding new questions)

1. Add new fact to postgresql_db/models.py as well as the type of answer you are expecting from it and the summary (displayed definition on the front-end)
2. Add your new fact to nlp_service/services/response_strings.py in "fact_questions" by adding the question trying to answer the fact
3. If not answerable by a generic "yes or no" add the fact as a {name_of_fact}.txt file in nlp_service/rasa/text/fact/individual
4. If answerable by a generic "yes or no", add the fact name to nlp_service/init_rasa.py in "fact_names"


## Adding a new outcome or a response (this section is only useful for developed claim categories)

1. Add the outcome(s) you want to be checked by the ml_service to the desired developed claim categories in nlp_service/services/fact_service.py in "outcome_mapping"
2. Tell the system what to say if the ml_service returns the outcome as "True" (it will happen) or "False" (it won't happen) in nlp_service/services/response_strings.py in "prediction"

## Retrain models

**The models are retrained every time the project is (re)built.**

The training is initialized init.py whenever the train function's force_train parameter inside of nlp_service/rasa/rasa_classifier.py is set to true.
The models are loaded in nlp_service/controllers/nlp_controller.py where force_train is initialized as false and initialize_interpreter is initialized as true.

# Working with RASA

The team a core part of its Natural Language Processing component [RASA NLU](https://github.com/RasaHQ/rasa_nlu).
Documentation available [here](https://rasa-nlu.readthedocs.io/en/latest/).
Active Gitter channel available [here](https://gitter.im/RasaHQ/rasa_nlu).

### Configuration:

The team experimented with multiple pipelines and considered Spacy 2.0 by far superior to MITIE.
Our config file can be found ~/nlp_service/rasa/config/rasa_config.json

**Components:**
- nlp_spacy: initializes spacy structures
- tokenizer_spacy: creation of tokens using Spacy
- intent_entity_featurizer_regex: uses regular expressions to aid in intent and entity classification (ONLY SUPPORTED BY NER_CRF)
- ner_crf: entity extractor using conditional random fields
- ner_synonyms: maps two or more entities to be extracted to have the same value
- intent_classifier_sklearn: classifies intents of the text being parsed
- duckling: extraction of pre-trained entities such as money, time, dates, etc.

We do not recommend "ner_spacy" as a replacement to "ner_crf" due to its absence of confidence scores for the entity extraction.
We also **strongly** advise against using more than 1 thread or more than 1 process due to stability issues with duckling.

### Achieving results:

Things to know that are not mentioned in RASA documentation:
* Proper usage of the intent_entity_featurizer_regex will often drastically improve intent confidence percentage (up to 40%)
  * Regex on sections of common examples that are unique to a specific intent
  (e.g.Regex on the word "tax" that has an extremely large chance of only appearing when the user wants information concerning his RL-31 slip)
  * Regex only actually helps with intent confidence ratio, not entity confidence.  (This bit of information was obtained after a conversation with RASA contributors on gitter)
* Working with common examples
  * I'm and Im and I am count as different words with Spacy. Avoid using those words in common examples.
  * Capitals matter. Lower casing our data sets while continuously lower casing the user's input for NLP improved the confidence percentage drastically
  * Avoid fluff (stop words) in the common examples for a proper word vector to be calculated.
  (e.g. deleting "can you help me with this?" at the end of the common examples for this will alter the vector calculated for the intent's common example.)
* Working with entities
    * We strongly suggest using entity_synonyms not only for different variations of the entity you are attempting to extract but also for common spelling mistakes of the entities

