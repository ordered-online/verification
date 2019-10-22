import json
import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse

from .sessions import UserSessionStore, UserSession


def verify_with_credentials(request):
    """Simple credientials based authentication via POST."""
    if request.method != "POST":
        return JsonResponse({"success": False})

    data = json.loads(request.body)
    user = authenticate(
        username=data.get("username"),
        password=data.get("password")
    )

    if user is None:
        return JsonResponse({"success": False})

    # Delete the old session, if it exists
    try:
        UserSession.objects.get(user_id__exact=user.id).delete()
    except UserSession.DoesNotExist:
        pass

    # Create a new user session
    session_store = UserSessionStore()
    session_store["user_id"] = user.id
    session_store.create()

    return JsonResponse({
        "session_key": session_store.session_key,
        "session_data": session_store.load(),
    })


def verify_with_session_key(request):
    """Simple session key based authentication via POST."""
    if request.method != "POST":
        return JsonResponse({"success": False})

    data = json.loads(request.body)
    session_key = data.get("session_key")

    if session_key is None:
        return JsonResponse({"success": False})

    try:
        session = UserSession.objects.get(pk=session_key)
    except UserSession.DoesNotExist:
        return JsonResponse({"success": False})

    return JsonResponse({
        "session_key": session_key,
        "session_data": session.get_decoded(),
    })


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
        return JsonResponse({"success": False})
    if len(username) < 4 or len(password) < 7:
        return JsonResponse({"success": False})
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return JsonResponse({"success": False})

    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
    except IntegrityError:
        return JsonResponse({"success": False})

    if user is None:
        return JsonResponse({"success": False})

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

    return JsonResponse({
        "session_key": session_store.session_key,
        "session_data": session_store.load(),
    })
