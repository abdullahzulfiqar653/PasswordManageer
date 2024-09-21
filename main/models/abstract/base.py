from django.db import models
from django.contrib.auth.models import User

from main.models.mixins.uid import UIDMixin


class BaseModel(models.Model, UIDMixin):
    id = models.CharField(max_length=15, primary_key=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.set_uid()
        super().save(**kwargs)
