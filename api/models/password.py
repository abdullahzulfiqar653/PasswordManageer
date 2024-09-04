from django.db import models
from api.models.base import BaseModel


class Password(BaseModel):
    url = models.URLField(null=True)
    notes = models.TextField(null=True)
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    emoji = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="passwords"
    )

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ["title", "username", "url", "user"]
