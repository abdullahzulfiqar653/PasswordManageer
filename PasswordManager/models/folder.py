from django.db import models
from main.models.abstract.base import BaseModel


class Folder(BaseModel):
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="folders"
    )
    title = models.CharField(max_length=255)
