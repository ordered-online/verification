# ordered online verification service

This django based micro service provides an API to verify users through auth tokens.

## Technology Stack

- Python 3
- Django

## Quickstart

Make sure, that Python 3 and Django are installed. Run the server.
```
$ cd verification
$ python3 manage.py migrate
$ python3 manage.py runserver
```

## API Endpoints

Example response if unsuccessful:
```json
{
  "success": false
}
```

Following API Endpoints are supported:

### `/verification/register/`
Register a new user with credentials. Returns the generated auth token.
Method: POST

Example with `curl`:
```
$ curl -i -X POST -H 'Content-Type: application/json' -d '{"username": "testuser", "password": "testtest", "email": "test@example.com", "first_name": "Test", "last_name": "User"}' http://127.0.0.1:8000/verification/register/

{
    "key": "1e5226b08111ec0f09f36f7d30105f61bd34cdfd",
    "user": 2,
    "timestamp": "2019-10-21T11:39:53.578Z"
}
```

### `/verification/verify/`
Verify an user with an authentication token. Returns the associated user.
Method: POST

Example with `curl`:
```
$ curl -i -X POST -H 'Content-Type: application/json' -d '{"token": "1e5226b08111ec0f09f36f7d30105f61bd34cdfd"}' http://127.0.0.1:8000/verification/verify/

{
    "key": "1e5226b08111ec0f09f36f7d30105f61bd34cdfd",
    "user": 2,
    "timestamp": "2019-10-21T11:39:53.578Z"
}
```

### `/verification/login/`
Verify an user with login credentials. Returns an authentication token.
Method: POST

Example with `curl`:
```
$ curl -i -X POST -H 'Content-Type: application/json' -d '{"username": "testuser", "password": "testtest"}' http://127.0.0.1:8000/verification/login/

{
    "key": "1e5226b08111ec0f09f36f7d30105f61bd34cdfd",
    "user": 2,
    "timestamp": "2019-10-21T11:39:53.578Z"
}
```

