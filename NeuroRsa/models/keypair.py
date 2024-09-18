from django.db import models
from django.contrib.auth.models import User

from main.models.abstract.base import BaseModel


class KeyPair(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="keypairs")
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    passphrase = models.CharField(max_length=64, null=True)
    private_key = models.TextField()
    public_key = models.TextField()
    is_main = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "name")

    def __str__(self):
        return f"{self.user.username} - {self.name}"
