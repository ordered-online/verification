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
    "session_key": "5qaff6u2ab0t0q0j0374xjhtya6uhwnx",
    "session_data": {
        "user_id": 1
    }
}
```

### `/verification/verify/session-key/`
Verify an user with a session key. Returns the associated user and a new session key.
Method: POST

Example with `curl`:
```
$ curl -i -X POST -H 'Content-Type: application/json' -d '{"session_key": "5qaff6u2ab0t0q0j0374xjhtya6uhwnx"}' http://127.0.0.1:8000/verification/verify/session-key/

{
    "session_key": "5qaff6u2ab0t0q0j0374xjhtya6uhwnx",
    "session_data": {
        "user_id": 1
    }
}
```

### `/verification/verify/credentials/`
Verify an user with login credentials. Returns an authentication token.
Note, that every time credentials are requested, all existing sessions from the user get invalidated.
Method: POST


Example with `curl`:
```
$ curl -i -X POST -H 'Content-Type: application/json' -d '{"username": "testuser", "password": "testtest"}' http://127.0.0.1:8000/verification/verify/credentials/

{
    "token": "3afexnw4gqoze0p3wt0nyd6nmmnzu4ek",
    "session": {
        "user_id": 1
    }
}
```

