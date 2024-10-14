from django.db import models
from django.contrib.auth.models import User

from main.models.abstract.base import BaseModel


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="public/user/profile/", null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
