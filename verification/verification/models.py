import binascii
import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Token(models.Model):
    """
    Represent a token.

    Tokens are used to log into our service.
    """
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["timestamp"]
        indexes = [
            models.Index(fields=["key"]),
        ]

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode()
        return super().save(*args, **kwargs)

    @property
    def json_serializable(self):
        return {
            "key": self.key,
            "user": self.user.id,
            "timestamp": self.timestamp
        }

    def __str__(self):
        return self.key
