from django.db import models

from django.utils import timezone
from main.models.abstract.base import BaseModel
from main.models.subscription import Subscription
from main.models.subscription_product_feature import SubscriptionProductFeature


class Feature(BaseModel):
    class Code(models.TextChoices):
        NUMBER_OF_MAILBOX = "number-of-mailbox"
        STORAGE_GB_EACH_MAILBOX = "storage-gb-each-mailbox"

    name = models.CharField(max_length=100)
    code = models.CharField(choices=Code.choices, max_length=100, unique=True)
    products = models.ManyToManyField(
        "main.SubscriptionProduct", through="SubscriptionProductFeature"
    )
    unit = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    default = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Feature"
        verbose_name_plural = "Product Features"

    @staticmethod
    def get_feature_value(feature_code, user):
        feature = Feature.objects.get(code=feature_code)
        product_feature = SubscriptionProductFeature.objects.filter(
            product__subscriptions__user=user,
            product__subscriptions__status__in=[
                Subscription.Status.ACTIVE,
            ],
            product__subscriptions__end_at__gt=timezone.now(),
            feature=feature,
        ).first()
        return product_feature.value if product_feature else feature.default
