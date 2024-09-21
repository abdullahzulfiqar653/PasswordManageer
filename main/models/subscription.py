from django.db import models
from django.contrib.auth.models import User

from main.models.abstract.base import BaseModel


class Subscription(BaseModel):
    class Status(models.TextChoices):
        # Ref: The complete list is in https://docs.stripe.com/api/subscriptions/object#subscription_object-status
        ACTIVE = "active"
        UNPAID = "unpaid"
        PAUSED = "paused"
        TRIALING = "trialing"
        PAST_DUE = "past_due"
        CANCELED = "canceled"
        INCOMPLETE = "incomplete"
        INCOMPLETE_EXPIRED = "incomplete_expired"

    end_at = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    started_at = models.DateTimeField(auto_now_add=True)
    is_free_trial = models.BooleanField(default=True)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="subscription",
    )
    product = models.ForeignKey(
        "main.SubscriptionProduct",
        on_delete=models.SET_NULL,
        null=True,
        related_name="subscriptions",
    )

    def __str__(self):
        return f"{self.product.name} - ({self.user.username})"

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
