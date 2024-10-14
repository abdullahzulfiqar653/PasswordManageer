from django.db import models
from main.models.abstract.base import BaseModel


class Password(BaseModel):
    url = models.CharField(max_length=255, null=True)
    notes = models.TextField(null=True)
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    emoji = models.CharField(max_length=10, null=True)
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="passwords"
    )
    folder = models.ForeignKey(
        "PasswordManager.Folder",
        on_delete=models.CASCADE,
        related_name="folder_passwords",
    )

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ["title", "username", "url", "user"]
