# Beta Server

Requires the following installed on the host system:
- SQLite
- Python3

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


