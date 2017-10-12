# Initialize a new conversation

Initializes a new conversation

**URL** : `/new`

**Method** : `POST`

**Data constraints**

Provide the user's name

```json
{
    "name": "[unicode 40 chars max]"
}
```
## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "conversation_id": 1
}
```

---

# Send a message

Sends a message to the bot.

**URL** : `/conversation`

**Method** : `POST`

**Data constraints**

Provide the conversation_id and a message. Message should be empty string for first call.

```json
{
    "conversation_id": "[integer]",
    "message": "[unicode]"
}
```
## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "conversation_id": 1,
    "message": "Hello Tim Timmens, are you a landlord or a tenant?"
}
```

## Error Response

**Code** : `404 Not Found`

---

# Get a conversation history

Gets the message history for a conversation

**URL** : `/conversation/:conversation_id`

**Method** : `GET`

## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "id": 1,
    "name": "Tim Timmens",
    "person_type": "TENANT",
    "messages": [
        {
            "id": 1,
            "sender_type": "BOT",
            "text": "Nice to meet you Tim Timmens, are you a landlord or a tenant?",
            "timestamp": "2017-10-12T00:00:36+00:00"
        },
        {
            "id": 2,
            "sender_type": "USER",
            "text": "I'm a tenant.",
            "timestamp": "2017-10-12T00:00:42+00:00"
        },
        {
            "id": 3,
            "sender_type": "BOT",
            "text": "What's your issue as a tenant?",
            "timestamp": "2017-10-12T00:00:42+00:00"
        },
        {
            "id": 4,
            "sender_type": "USER",
            "text": "My landlord is trying to raise my rent, but my lease ends in 4 months.",
            "timestamp": "2017-10-12T00:00:50+00:00"
        },
        {
            "id": 5,
            "sender_type": "BOT",
            "text": "Did your landlord give you any warning of the rent increase in advance?",
            "timestamp": "2017-10-12T00:00:50+00:00"
        }
    ],

}
```

## Error Response

**Code** : `400 Bad Request`

**Code** : `404 Not Found`