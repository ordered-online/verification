from django.contrib.auth.models import User
from django.contrib.sessions.base_session import AbstractBaseSession
from django.contrib.sessions.backends.db import SessionStore
from django.db import models


class UserSession(AbstractBaseSession):
    """Represent a user related session."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @classmethod
    def get_session_store_class(cls):
        return UserSessionStore


class UserSessionStore(SessionStore):
    @classmethod
    def get_model_class(cls):
        return UserSession

    def create_model_instance(self, data):
        obj = super().create_model_instance(data)
        obj.user_id = self["user_id"]
        return obj
