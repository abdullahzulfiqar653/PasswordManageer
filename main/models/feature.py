from django.db import models

from main.models.abstract.base import BaseModel


class Feature(BaseModel):
    class Code(models.TextChoices):
        NUMBER_OF_EMAILS = "number-of-emails"
        STORAGE_GB_EACH_EMAIL = "storage-gb-each-email"

    name = models.CharField(max_length=100)
    code = models.CharField(choices=Code.choices, max_length=100, unique=True)
    products = models.ManyToManyField(
        "main.SubscriptionProduct", through="SubscriptionProductFeature"
    )
    unit = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    default = models.FloatField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Feature"
        verbose_name_plural = "Product Features"
