# Backend Service

## Run Tests and Lints

```
export COMPOSE_FILE=ci
./cjl up -d && ./cjl run backend_service
```

---
# Backend API

# Initialize a new conversation

Initializes a new conversation

**URL** : `/new`

**Method** : `POST`

**Data constraints**

Provide the user's name and person type.

```json
{
    "name": "[unicode 40 chars max]",
    "person_type": "(TENANT|LANDLORD)"
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

## Error Response

**Code** : `400 Bad Request` - *Invalid person_type provided*

---

# Store User Confirmation

Stores the user confirmation or text supplied in order to confirm whether an NLP prediction was accurate.

**URL** : `/store-user-confirmation`

**Method** : `POST`

**Data constraints**

Provide the conversation id and confirmation text of the user.

```json
{
    "conversation_id": 1,
    "confirmation": true | false | "$5000"
}
```

## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "message": "User confirmation stored successfully"
}
```

## Error Response

**Code** : `400 Bad Request`

**Code** : `404 Not Found`

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

Simple response containing a message. Messages may contain pipe characters (|) which indicate that a sentence should be split into separate conversation windows. Note that the first message will not contain a pipe character. Each subsequent sentence will begin with a pipe character if it is meant to be split.

### Example 1:

```json
{
    "conversation_id": 1,
    "message": "Hello Tim Timmens!|What kind of problem are you having?"
}
```

This can be formatted as:

Message 1: Hello Tim Timmens!

Message 2: What kind of problem are you having?

### Example 2:

```json
{
    "conversation_id": 5,
    "message": "Oh I see you're having problems with lease termination!|I have a few questions for you.|Do you have a lease?"
}
```

This can be formatted as:

Message 1: Oh I see you're having problems with lease termination!

Message 2: I have a few questions for you.

Message 3: Do you have a lease


### Response containing a request for a file.

```json
{
    "conversation_id": 1,
    "file_request": {
        "document_type": "LEASE"
    },
    "message": "Could you please upload your lease if you have it, Tim Timmens?"
}
```

### Document Types

*LEASE*: A lease for a dwelling

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
	"claim_category": "NONPAYMENT",
	"current_fact": {
		"name": "landlord_retakes_apartment",
		"summary": "Landlord intends to retake dwelling",
		"type": "BOOLEAN"
	},
	"fact_entities": [
		{
			"fact": {
				"name": "apartment_impropre",
				"summary": "Dwelling unfit for habitation",
				"type": "BOOLEAN"
			},
			"id": 1,
			"value": "false"
		},
		{
			"fact": {
				"name": "landlord_relocation_indemnity_fees",
				"summary": "Relocation reimbursed following inhabitability",
				"type": "BOOLEAN"
			},
			"id": 2,
			"value": "true"
		}
	],
	"files": [],
	"id": 1,
	"messages": [
		{
			"enforce_possible_answer": true,
			"file_request": null,
			"id": 1,
			"possible_answers": "[\"Yes\"]",
				"relevant_fact": null,
				"sender_type": "BOT",
				"text": "Hello Bobby! Before we start, I want to make it clear that I am not a replacement for a lawyer and any information I provide you with is not meant to be construed as legal advice. Always check in with your legal professional. You can read more about our terms of use <a href='/legal' target='_blank'>here</a>. Do you accept these conditions?",
				"timestamp": "2017-12-20T01:27:35.993932+00:00"
			},
			{
				"enforce_possible_answer": null,
				"file_request": null,
				"id": 2,
				"possible_answers": null,
				"relevant_fact": null,
				"sender_type": "USER",
				"text": "Yes",
				"timestamp": "2017-12-20T01:27:39.023317+00:00"
			},
			{
				"enforce_possible_answer": false,
				"file_request": {
					"document_type": "LEASE"
				},
				"id": 3,
				"possible_answers": null,
				"relevant_fact": null,
				"sender_type": "BOT",
				"text": "I see you're a tenant, Bobby. If you have it on hand, it would be very helpful if you could upload your lease. What issue can I help you with today?",
				"timestamp": "2017-12-20T01:27:39.040375+00:00"
			},
			{
				"enforce_possible_answer": null,
				"file_request": null,
				"id": 4,
				"possible_answers": null,
				"relevant_fact": null,
				"sender_type": "USER",
				"text": "I am being kicked out",
				"timestamp": "2017-12-20T01:27:40.694884+00:00"
			},
			{
				"enforce_possible_answer": false,
				"file_request": null,
				"id": 5,
				"possible_answers": null,
				"relevant_fact": {
					"name": "apartment_impropre",
					"summary": "Dwelling unfit for habitation",
					"type": "BOOLEAN"
				},
				"sender_type": "BOT",
				"text": "Oh yes, I know all about problems with nonpayment. Would you deem the apartment unfit for habitation?",
				"timestamp": "2017-12-20T01:27:40.794129+00:00"
			},
			{
				"enforce_possible_answer": null,
				"file_request": null,
				"id": 6,
				"possible_answers": null,
				"relevant_fact": {
					"name": "apartment_impropre",
					"summary": "Dwelling unfit for habitation",
					"type": "BOOLEAN"
				},
				"sender_type": "USER",
				"text": "No",
				"timestamp": "2017-12-20T01:28:46.591573+00:00"
			},
			{
				"enforce_possible_answer": false,
				"file_request": null,
				"id": 7,
				"possible_answers": null,
				"relevant_fact": {
					"name": "landlord_relocation_indemnity_fees",
					"summary": "Relocation reimbursed following inhabitability",
					"type": "BOOLEAN"
				},
				"sender_type": "BOT",
				"text": "Have moving expenses been compensated when the apartment was deemed inhabitable?",
				"timestamp": "2017-12-20T01:28:46.652110+00:00"
			},
			{
				"enforce_possible_answer": null,
				"file_request": null,
				"id": 8,
				"possible_answers": null,
				"relevant_fact": {
					"name": "landlord_relocation_indemnity_fees",
					"summary": "Relocation reimbursed following inhabitability",
					"type": "BOOLEAN"
				},
				"sender_type": "USER",
				"text": "Yes",
				"timestamp": "2017-12-20T01:28:51.529825+00:00"
			}
		],
	"name": "Bobby",
	"person_type": "TENANT"
}
```

## Error Response

**Code** : `400 Bad Request`

**Code** : `404 Not Found`

---
# Get facts resolved during conversation

Gets only the list of resolved facts for the conversation

**URL** : `/conversation/:conversation_id/resolved`

**Method** : `GET`

## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
	"fact_entities": [
		{
			"fact": {
				"name": "apartment_impropre",
				"summary": "Dwelling unfit for habitation",
				"type": "BOOLEAN"
			},
            "id": 1,
			"value": "false"
		},
		{
			"fact": {
				"name": "landlord_relocation_indemnity_fees",
				"summary": "Relocation reimbursed following inhabitability",
				"type": "BOOLEAN"
			},
            "id": 2,
			"value": "true"
		}
	]
}
```

## Error Response

**Code** : `400 Bad Request`

**Code** : `404 Not Found`

---
# Remove a resolved fact

Removes a resolved fact from the conversation

**URL** : `/conversation/:conversation_id/resolved/:fact_id`

**Method** : `DELETE`

## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
	"success": true
}
```

## Error Response

**Code** : `400 Bad Request`

**Code** : `404 Not Found`

---

# Upload a file 

Upload a file that serves as evidence for a particular conversation.

**URL** : `/conversation/:conversation_id/files`

**Method** : `POST`

**Headers**

Content-Type: `multipart/form-data`

**Data constraints**

Provide 'file' form key with file data.

## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "name": "leaky_pipes.png",
    "type": "image/png",
    "timestamp": "2017-10-24T00:01:27.806730+00:00"
}
```

## Error Response

**Code** : `400 Bad Request`

**Code** : `404 Not Found`

---

# Get conversation file metadata

Gets a list of file metadata for a conversation

**URL** : `/conversation/:conversation_id/files`

**Method** : `GET`

## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
	"files": [
		{
			"name": "leaky_pipes.png",
			"type": "image/png",
			"timestamp": "2017-10-24T00:01:27.000000+00:00"
		},
		{
			"name": "my_least.pdf",
			"type": "application/pdf",
			"timestamp": "2017-10-24T00:01:30.000000+00:00"
		}
	]	
}
```

## Error Response

**Code** : `400 Bad Request`

**Code** : `404 Not Found`

---

# Get Latest Legal Documents

Obtains information and contents of the latest legal documents

**URL** : `/legal`

**Method** : `GET`

## Success Response

**Code** : `200 OK`

**Content examples**

```json
[
    {
        "abbreviation": "EULA",
        "html": {
            "content": [
                {
                    "subtitle": "TL;DR",
                    "summary": "no purse as fully me or point. Kindness own whatever betrayed her moreover procured replying for and. Proposal indulged no do do sociable he throwing settling. Covered ten nor comfort offices carried. Age she way earnestly the fulfilled extremely.",
                    "text": "Prevailed sincerity behaviour to so do principle mr. As departure at no propriety zealously my. On dear rent if girl view. First on smart there he sense. Earnestly enjoyment her you resources. Brother chamber ten old against. Mr be cottage so related minuter is. Delicate say and blessing ladyship exertion few margaret. Delight herself welcome against smiling its for. Suspected discovery by he affection household of principle perfectly he.",
                    "title": "DESCRIPTION OF SERVICE"
                },
                {
                    "subtitle": "TL;DR",
                    "summary": "Scarcely on striking packages by so property in delicate. Up or well must less rent read walk so be. Easy sold at do hour sing spot. Any meant has cease too the decay. Since party burst am it match. By or blushes between besides offices noisier as.",
                    "text": "It prepare is ye nothing blushes up brought. Or as gravity pasture limited evening on. Wicket around beauty say she. Frankness resembled say not new smallness you discovery. Noisier ferrars yet shyness weather ten colonel. Too him himself engaged husband pursuit musical. Man age but him determine consisted therefore. Dinner to beyond regret wished an branch he. Remain bed but expect suffer little repair.",
                    "title": "ACCEPTANCE OF TERMS"
                },
                {
                    "subtitle": "TL;DR",
                    "summary": "Luckily friends do ashamed to do suppose. Tried meant mr smile so. Exquisite behaviour as to middleton perfectly.",
                    "text": "He my polite be object oh change. Consider no mr am overcame yourself throwing sociable children. Hastily her totally conduct may. My solid by stuff first smile fanny. Humoured how advanced mrs elegance sir who. Home sons when them dine do want to. Estimating themselves unsatiable imprudence an he at an. Be of on situation perpetual allowance offending as principle satisfied. Improved carriage securing are desirous too.",
                    "title": "MODIFICATION OF TERMS"
                },
                {
                    "subtitle": "TL;DR",
                    "summary": "Improved own provided blessing may peculiar domestic. Sight house has sex never. No visited raising gravity outward subject my cottage mr be. Hold do at tore in park feet near my case.",
                    "text": "Extremely we promotion remainder eagerness enjoyment an. Ham her demands removal brought minuter raising invited gay. Contented consisted continual curiosity contained get sex. Forth child dried in in aware do. You had met they song how feel lain evil near. Small she avoid six yet table china. And bed make say been then dine mrs. To household rapturous fulfilled attempted on so. ",
                    "title": "REGISTRATION"
                }
            ],
            "header": "End User License Agreement",
            "subheader": "Savings her pleased are several started females met. Short her not among being any. Thing of judge fruit charm views do. Miles mr an forty along as he. She education get middleton day agreement performed preserved unwilling. Do however as pleased offence outward beloved by present. By outward neither he so covered amiable greater. Juvenile proposal betrayed he an informed weddings followed. Precaution day see imprudence sympathize principles. At full leaf give quit to in they up."
        },
        "time_created": "2017-10-26T20:52:41-04:00",
        "type": "End User License Agreement",
        "version": 1
    }
]
```
