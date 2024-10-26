from django.db import models
from django.contrib.auth.models import User

from main.models.abstract.base import BaseModel


class Recipient(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipients")
    name = models.CharField(max_length=255)
    public_key = models.TextField()
    emoji = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        unique_together = ("user", "name")

    def __str__(self):
        return f"{self.user.username} - {self.name}"
