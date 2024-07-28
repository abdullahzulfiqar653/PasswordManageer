from django.db import models
from api.models.base import BaseModel
from django.contrib.auth.models import User


class KeyPair(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    private_key = models.TextField()
    public_key = models.TextField()

    class Meta:
        unique_together = ("user", "name")

    def __str__(self):
        return f"{self.user.username} - {self.name}"
