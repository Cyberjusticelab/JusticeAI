# Natural Language Processing Service

## Run Tests and Lints

```
export COMPOSE_FILE=ci
./cjl up -d && ./cjl run nlp_service
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
    "message": "I see you're having problems with lease termination. Have you kept up with your rent payments?"
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
    "message": "Have you kept up with your rent payments?"
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
() = entity_name1,entity_extractor(optional)
{} = entity_name2,entity_extractor(optional)

[regex_features]
name:regex

[entity_synonyms]
entity:synonym1, synonym2

[common_examples:intent_name1]
sentence1
sentence2

[common_examples:intent_name2]
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
() = money,ner_duckling

[regex_features]
money:$\d(.)?+|\d(.)?+$

[common_examples:true]
my landlord increased my rent by ($500)
i owe my landlord (40 dollars)

[common_examples:false]
i don't owe my landlord any money
i dont have any debts
no
```

### Command Line Use
python3 -m util.parse_dataset <read_dir> <write_dir>

#### Example
python3 -m util.parse_dataset ~/Documents/ ~/Documents/Json/

**DO NOT FORGET THE '/' AT THE END OF YOUR DIRECTORY**