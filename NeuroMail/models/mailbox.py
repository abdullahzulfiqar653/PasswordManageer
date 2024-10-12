from django.db import models
from django.contrib.auth.models import User

from main.models.abstract.base import BaseModel


class MailBox(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mailboxes")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.email}"
