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
$ python3 manage.py runserver 127.0.0.1:8000
```
