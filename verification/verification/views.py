import json
import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse

from .sessions import UserSessionStore, UserSession


class SuccessResponse(JsonResponse):
    def __init__(self, response=None):
        if response is None:
            super().__init__({
                "success": True,
            })
        else:
            super().__init__({
                "success": True,
                "response": response
            })


class AbstractFailureResponse(JsonResponse):
    reason = None

    def __init__(self):
        super().__init__({
            "success": False,
            "reason": self.reason
        })


class IncorrectCredentials(AbstractFailureResponse):
    reason = "incorrect_credentials"


class IncorrectAccessMethod(AbstractFailureResponse):
    reason = "incorrect_access_method"


class IncorrectSessionKey(AbstractFailureResponse):
    reason = "incorrect_session_key"


class IncorrectUserId(AbstractFailureResponse):
    reason = "incorrect_user_id"


class DuplicateUser(AbstractFailureResponse):
    reason = "duplicate_user"


def login(request):
    """Simple credientials based authentication via POST."""
    if request.method != "POST":
        return IncorrectAccessMethod()

    data = json.loads(request.body)
    user = authenticate(
        username=data.get("username"),
        password=data.get("password")
    )

    if user is None:
        return IncorrectCredentials()

    # Delete the old session, if it exists
    try:
        UserSession.objects.get(user_id__exact=user.id).delete()
    except UserSession.DoesNotExist:
        pass

    # Create a new user session
    session_store = UserSessionStore()
    session_store["user_id"] = user.id
    session_store.create()

    return SuccessResponse({
        "session_key": session_store.session_key,
        "session_data": session_store.load(),
    })


def logout(request):
    """Logout a user by deleting his session via POST."""
    if request.method != "POST":
        return IncorrectAccessMethod()

    data = json.loads(request.body)
    session_key = data.get("session_key")
    user_id = data.get("user_id")

    if session_key is None:
        return IncorrectSessionKey()

    if user_id is None:
        return IncorrectUserId()

    try:
        session = UserSession.objects.get(pk=session_key)
    except UserSession.DoesNotExist:
        return IncorrectSessionKey()

    if session.user_id != user_id:
        return IncorrectUserId()

    session.delete()

    return SuccessResponse()


def verify(request):
    """Simple session key based authentication via POST."""
    if request.method != "POST":
        return IncorrectAccessMethod()

    data = json.loads(request.body)
    session_key = data.get("session_key")
    user_id = data.get("user_id")

    if session_key is None:
        return IncorrectSessionKey()

    if user_id is None:
        return IncorrectUserId()

    try:
        session = UserSession.objects.get(pk=session_key)
    except UserSession.DoesNotExist:
        return IncorrectSessionKey()

    if session.user_id != user_id:
        return IncorrectUserId()

    return SuccessResponse()


def register(request):
    """Simple user registration via POST."""
    if request.method != "POST":
        return JsonResponse({"success": False})

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    if not username or not password or not email or not first_name or not last_name:
        return IncorrectCredentials()
    if len(username) < 4 or len(password) < 7:
        return IncorrectCredentials()
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return IncorrectCredentials()

    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
    except IntegrityError:
        return DuplicateUser()

    if user is None:
        return IncorrectCredentials()

    # Delete the old session, if it exists.
    # This could happen, if a user was deleted beforehand
    # but left his session behind
    try:
        UserSession.objects.get(user_id__exact=user.id).delete()
    except UserSession.DoesNotExist:
        pass

    session_store = UserSessionStore()
    session_store["user_id"] = user.id
    session_store.create()

    return SuccessResponse({
        "session_key": session_store.session_key,
        "session_data": session_store.load(),
    })
