from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse

from auth.auth.models import Token


def login_with_credentials(request):
    """Simple credientials based authentication via POST."""
    if request.method != "POST":
        return JsonResponse({"success": False})
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({"success": False})
    return JsonResponse(serializers.serialize("json", user.token))


def login_with_auth_token(request):
    """Simple token based authentication via POST."""
    if request.method != "POST":
        return JsonResponse({"success": False})
    token = request.POST.get("token")
    user = authenticate(token=token)
    if not user:
        return JsonResponse({"success": False})
    return JsonResponse(serializers.serialize("json", user.token))


def register(request):
    """Simple user registration via POST."""
    if request.method != "POST":
        return JsonResponse({"success": False})
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    if not username or not password or not email:
        return JsonResponse({"success": False})
    if len(username) < 4 or len(password) < 8:
        return JsonResponse({"success": False})
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    if not user:
        return JsonResponse({"success": False})
    Token.objects.create(user=user)
    return JsonResponse(serializers.serialize("json", user.token))
