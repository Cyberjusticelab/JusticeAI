# Natural Language Processing Service

## Run Tests and Lints

```
export COMPOSE_FILE=ci
./cjl up -d && ./cjl run nlp_service
```

---
# NLP API

# Submit answer

Submits a user input to the NLP service. Returns the next question to ask.

**URL** : `/submit_answer`

**Method** : `POST`

**Data constraints**

Provide the conversation id and the message.

```json
{
    "conversation_id": 1,
    "message": "My rent is $900 per month."
}
```
## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "message": "Have you kept up with your rent payments?"
}
```

## Error Response

**Code** : `400 Bad Request` - *Inputs not provided*

**Code** : `404 Not Found` - *Conversation doesn't exist*

---