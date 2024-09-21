from django.db import models
from django.utils import timezone

from main.models.abstract.base import BaseModel


def get_date(timestamp):
    return timezone.datetime.fromtimestamp(timestamp, tz=timezone.utc)


class SubscriptionProduct(BaseModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    @classmethod
    def update_or_create(cls, product_data):
        obj, created = cls.objects.update_or_create(
            id=product_data["id"],
            defaults={
                "name": product_data["name"],
                "is_active": product_data["active"],
                "created_at": get_date(product_data["created"]),
                "updated_at": get_date(product_data["updated"]),
            },
        )
        return obj, created
