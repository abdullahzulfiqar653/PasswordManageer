from django.db import models
from shortuuid.django_fields import ShortUUIDField


class BaseModel(models.Model):
    id = ShortUUIDField(length=12, max_length=12, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
