# ordered online verification service

This django based micro service provides an API to verify users through auth tokens.

The core idea of this service is to encapsulate the user management and make it available via given interfaces.

Example: The web client stores all user authentication related data, which is the `user_id` and the `session_key`. Both are obtained through registration or login, respectively. Then the web client sends this data to a service, which needs authentication. The called web service verifies the user through the given information and gives the user access to its resources. The service itself only has to keep the mapping between resources and their associated user id.


## Technology Stack

- Python 3
- Django

## Quickstart

```
$ python3 -m pip install -r verification/requirements.txt
```

Run the server in development mode.
```
$ cd verification
$ python3 manage.py migrate
$ python3 manage.py runserver 127.0.0.1:8001
```

## API Endpoints

Following API Endpoints are supported:

### Registration via `/verification/register/`
Register a new user with credentials. Returns the generated auth token.
Method: POST


|Parameter|Restriction|Mandatory|
|-|-|-|
|username|Should be longer than 4 characters.|yes|
|password|Should be sufficiently complex and longer than 7 characters.|yes|
|email|Should be a valid email.|yes|
|first_name|None|yes|
|last_name|None|yes|

Example with `curl`:
```
$ curl -i -X POST -H 'Content-Type: application/json' -d '{"username": "testuser", "password": "testtest", "email": "test@example.com", "first_name": "Test", "last_name": "User"}' http://127.0.0.1:8001/verification/register/

{
    "success": true,
    "response": {
        "session_key": "4zn5tlb1psfv7o8vurrtactbis76aw9m",
        "session_data": {
            "user_id": 1
        }
    }
}
```

Failure responses:
- [MalformedJson](#MalformedJson) if the passed json could not be read from the request body.
- [IncorrectAccessMethod](#IncorrectAccessMethod) if the service was accessed with any other method than specified.
- [IncorrectCredentials](#IncorrectCredentials) if the supplied credentials are insufficient for account creation.
- [DuplicateUser](#DuplicateUser) if the user already exists.

### Session key verification via`/verification/verify/`
Verify a user with a session key. Returns the associated user and a new session key.
Method: POST

|Parameter|Restriction|Mandatory|
|-|-|-|
|session_key|Should be a valid session key.|yes|
|user_id|Should be a valid user_id which is associated to the session.|yes|

Note that `user_id` is required to avoid brute force style attacks.

Example with `curl`:
```
$ curl -i -X POST -H 'Content-Type: application/json' -d '{"session_key": "lyp1u0ld51p42mnv1jcw8qqqe5iijt3p", "user_id": 1}' http://127.0.0.1:8001/verification/verify/

{
    "success": true,
    "response": {
        "session_key": "4zn5tlb1psfv7o8vurrtactbis76aw9m",
        "session_data": {
            "user_id": 1
        }
    }
}
```

Failure responses:
- [MalformedJson](#MalformedJson) if the passed json could not be read from the request body.
- [IncorrectAccessMethod](#IncorrectAccessMethod) if the service was accessed with any other method than specified.
- [IncorrectSessionKey](#IncorrectSessionKey) if the session key is incorrect or the accessed session no longer exists.
- [IncorrectUserId](#IncorrectUserId) if the given user id is incorrect.

### Login via `/verification/login/`
Verify an user with login credentials. Returns an authentication token.
Note, that every time credentials are requested, all existing sessions from the user get invalidated.
Method: POST

|Parameter|Restriction|Mandatory|
|-|-|-|
|username|Should be a valid username.|yes|
|password|Should be a valid password.|yes|

Example with `curl`:
```
$ curl -i -X POST -H 'Content-Type: application/json' -d '{"username": "testuser", "password": "testtest"}' http://127.0.0.1:8001/verification/login/ 

{
    "success": true,
    "response": {
        "session_key": "xnzafme15cgceeyhchdgahjdc72hzu9z",
        "session_data": {
            "user_id": 1
        }
    }
}
```

Failure Responses:
- [MalformedJson](#MalformedJson) if the passed json could not be read from the request body.
- [IncorrectAccessMethod](#IncorrectAccessMethod) if the service was accessed with any other method than specified.
- [IncorrectCredentials](#IncorrectCredentials) if the credentials are incorrect.

### Logout via `/verification/logout/`
Invalidate the session under the given session key and logout.
Method: POST

|Parameter|Restriction|Mandatory|
|-|-|-|
|session_key|Should be a valid session key.|yes|
|user_id|Should be a valid user_id which is associated to the session.|yes|

Note that `user_id` is required to avoid brute force style attacks.

Example with `curl`:
```
$ curl -i -X POST -H 'Content-Type: application/json' -d '{"session_key": "lyp1u0ld51p42mnv1jcw8qqqe5iijt3p", "user_id": 1}' http://127.0.0.1:8001/verification/logout/

{ 
   "success":true
}
```

Failure responses:
- [MalformedJson](#MalformedJson) if the passed json could not be read from the request body.
- [IncorrectAccessMethod](#IncorrectAccessMethod) if the service was accessed with any other method than specified.
- [IncorrectSessionKey](#IncorrectSessionKey) if the session key is incorrect or the accessed session no longer exists.
- [IncorrectUserId](#IncorrectUserId) if the given user id is incorrect.


## Failure Responses

Following failure responses are supported:

### MalformedJson

Code: 400

```
{
    "success":false,
    "reason":"malformed_json"
}
```

### IncorrectCredentials

Code: 403

```
{ 
   "success":false,
   "reason":"incorrect_credentials"
}
```

### IncorrectAccessMethod

Code: 405

```
{ 
   "success":false,
   "reason":"incorrect_access_method"
}
```

### IncorrectSessionKey

Code: 403

```
{ 
   "success":false,
   "reason":"incorrect_session_key"
}
```

### IncorrectUserId

Code: 403

```
{ 
   "success":false,
   "reason":"incorrect_user_id"
}
```

### DuplicateUser

Code: 400

```
{ 
   "success":false,
   "reason":"duplicate_user"
}
```

