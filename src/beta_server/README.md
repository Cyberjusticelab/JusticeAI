# Beta Server

Requires the following installed on the host system:
- SQLite
- Python3

## SETUP

`pip install -r requirements.txt`
`FLASK_APP=app.py flask run`

## REST API DOCUMENTATTION

### `POST /question`

Inserts a new user-generated question. Returns that user's ID.

#### Example request payload
```json
{
	"question": "Is it okay for a landlord to ask for a security deposit?"
}
```

#### Success response payload
```json
{
	"id": "5cd8a900-8a18-41b3-abb8-bf0307918afc"
}
```

#### Error response status codes
- `415` if request does not contain valid JSON
- `422` if the `question` key is not present
- `422` if the `question` value is too long

### `PUT /email`

Updates a user's email address based on their ID.

If an ID is provided, that ID's record is updated. If no ID is provided, a new record is created.


#### Example request payload
```json
{
	"id": "5c17bfd0-87d0-4493-a312-f3f32323fff2",
	"email": "test@test.com"
}
```

#### Success response payload
```json
{
	"id": "5c17bfd0-87d0-4493-a312-f3f32323fff2"
}
```

#### Error response status codes
- `415` if request does not contain valid JSON
- `422` if the `email` key is not present
- `422` if the `email` value is too long

### `PUT /subscription`

Updates a user's subscription status based on their ID. `1` is subscribed, `0` is not subscribed.

If an ID is provided, that ID's record is updated. If no ID is provided, a new record is created.

#### Example request payload
```json
{
	"id": "5c17bfd0-87d0-4493-a312-f3f32323fff2",
	"is_subscribed": 1
}
```

#### Success response payload
```json
{
	"id": "5c17bfd0-87d0-4493-a312-f3f32323fff2"
}
```

#### Error response status codes
- `415` if request does not contain valid JSON
- `422` if the `is_subscribed` key is not present
- `422` if the `is_subscribed` key is not an integer

### `PUT /legal`

Updates a user's status on whether they are a legal professional based on their ID. `1` is a legal professional, `0` is not.

If an ID is provided, that ID's record is updated. If no ID is provided, a new record is created.

#### Example request payload
```json
{
	"id": "5c17bfd0-87d0-4493-a312-f3f32323fff2",
	"is_legal_professional": 1
}
```

#### Success response payload
```json
{
	"id": "5c17bfd0-87d0-4493-a312-f3f32323fff2"
}
```

#### Error response status codes
- `415` if request does not contain valid JSON
- `422` if the `is_subscribed` key is not present
- `422` if the `is_subscribed` key is not an integer


