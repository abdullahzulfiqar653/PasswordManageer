from django.db import models

from main.models.abstract.base import BaseModel
from NeuroMail.models.email_box import EmailBox


class EmailBoxRecipient(BaseModel):
    TO = "to"
    CC = "cc"
    BCC = "bcc"

    RECIPIENT_TYPE_CHOICES = [
        (TO, "To"),
        (CC, "CC"),
        (BCC, "BCC"),
    ]

    email_box = models.ForeignKey(
        EmailBox, on_delete=models.CASCADE, related_name="recipients"
    )
    email = models.EmailField()
    recipient_type = models.CharField(max_length=3, choices=RECIPIENT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.email} ({self.recipient_type})"
