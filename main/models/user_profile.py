from django.db import models
from django.contrib.auth.models import User

from main.models.abstract.base import BaseModel


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image_name = models.CharField(max_length=256, null=True, blank=True)
    total_size = models.PositiveBigIntegerField(default=0)
    address = models.CharField(max_length=512, null=True, blank=True)
    
    def add_size(self, size):
        self.total_size += size
        self.save()

    def remove_size(self, size):
        if self.total_size - size < 0:
            self.total_size = 0
        else:
            self.total_size -= size
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Profile"
