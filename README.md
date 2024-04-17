# ops_api

API for Remote Updates to Snowflake Data

## Authentication

Authenticate your request by passing your API key as a bearer token in the authorization header

**Sample headers**

```
{'Authorization': 'Bearer <api_key>'}
```

## Endpoints

**/update-user**

**Description:**

Use this endpoint to update any column in the user table. Successfully calling this endpoint will directly update data in the user table and create a log record in the audit log events table.

**Required Args:**

- user_id - id from users table or voyager user_id
- data - JSON payload of updates to make. Keys should be column name (case insensitive) values should be new value to update to. All keys passed will attempt to be updated. If you pass a key that is not a column in the user table, the request will fail. Values are case sensative and will be updated exactly as passed. Be sure that the value passed for an update matches the format of the column that you are attempting an update on. Pass all values as strings.

**Sample Request**

Curl

```
url -X POST -H "Authorization: Bearer <api_key>" -d '{"state": "NJ", "city": "Newark", "zip": "08906"}' https://opsapi-production.up.railway.app/update_user?user_id=123456
```

Python

```
import requests

user_id = 123456
base_url = ''
url = f'{base_url}/update_user?user_id={user_id}'

api_key = '123456789'
headers = {
    'Authorization': f'Bearer {api_key}'
}

payload = {"state": "NJ", "city": "Newark", "zip": "08906"}

resp = request.post(url, headers=headers, json=paylod)
```

**Accepted Values**

- EMAIL
- FIRST_NAME
- LAST_NAME
- ADDRESS1
- ADDRESS2
- CITY
- STATE
- ZIP
- PHONE_COUNTRY_CODE
- PHONE
- COUNTRY_CODE
- IS_FOREIGN
- HAS_CLAIM
