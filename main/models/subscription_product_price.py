from django.db import models

from main.models.abstract.base import BaseModel


class SubscriptionProductPrice(BaseModel):
    product = models.ForeignKey(
        "main.SubscriptionProduct",
        on_delete=models.CASCADE,
        editable=False,
        related_name="product_prices",
    )
    is_active = models.BooleanField(default=True)
    nickname = models.CharField(max_length=256, null=True)
    recurring_interval = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.product.name

    @classmethod
    def update_or_create(cls, price_data):
        obj, created = cls.objects.update_or_create(
            id=price_data["id"],
            defaults={
                "product_id": price_data["product"],
                "is_active": price_data["active"],
                "nickname": price_data["nickname"],
                "recurring_interval": price_data["recurring"]["interval"],
                "price": price_data["price"],
            },
        )
        return obj, created
