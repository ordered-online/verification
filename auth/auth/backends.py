from django.contrib.auth.models import User

from auth.auth.models import Token


class AuthenticationHeaderTokenBackend:
    """
    Simple token based authentication.

    Example token: 401f7ac837da42b97f613d789819ff93537bee6a
    """

    def authenticate(self, request, token):
        if not token:
            return None
        try:
            token = Token.objects.select_related("user").get(key=token)
        except Token.DoesNotExist:
            return None
        return token.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
