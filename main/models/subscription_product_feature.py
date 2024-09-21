from django.db import models

from main.models.abstract.base import BaseModel


class SubscriptionProductFeature(BaseModel):
    product = models.ForeignKey(
        "main.SubscriptionProduct",
        on_delete=models.CASCADE,
        related_name="product_features",
    )
    feature = models.ForeignKey(
        "main.Feature", on_delete=models.CASCADE, related_name="product_features"
    )
    value = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.feature.name}: {self.value}"

    class Meta:
        verbose_name = "Product Feature Assignment"
        verbose_name_plural = "Product Feature Assignments"
        unique_together = ("product", "feature")
