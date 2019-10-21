import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import JsonResponse

from .models import Token


def login_with_credentials(request):
    """Simple credientials based authentication via POST."""
    if request.method != "POST":
        return JsonResponse({"success": False})
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"success": False})
    return JsonResponse(model_to_dict(user.token))


def verify_with_auth_token(request):
    """Simple token based authentication via POST."""
    if request.method != "POST":
        return JsonResponse({"success": False})
    data = json.loads(request.body)
    token = data.get("token")
    user = authenticate(token=token)
    if user is None:
        return JsonResponse({"success": False})
    return JsonResponse(model_to_dict(user.token))


def register(request):
    """Simple user registration via POST."""
    if request.method != "POST":
        return JsonResponse({"success": False})
    data = json.loads(request.body)
    print(data)
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    if not username or not password or not email or not first_name or not last_name:
        return JsonResponse({"success": False})
    if len(username) < 4 or len(password) < 7:
        return JsonResponse({"success": False})
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    if user is None:
        return JsonResponse({"success": False})
    Token.objects.create(user=user)
    return JsonResponse(model_to_dict(user.token))
