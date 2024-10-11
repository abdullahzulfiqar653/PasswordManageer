from django.db import models

from main.models.abstract.base import BaseModel
from NeuroMail.models.mailbox import MailBox


class MailBoxRecipient(BaseModel):
    UID_PREFIX = 122
    TO = "to"
    CC = "cc"
    BCC = "bcc"

    RECIPIENT_TYPE_CHOICES = [
        (TO, "To"),
        (CC, "CC"),
        (BCC, "BCC"),
    ]

    mail_box = models.ForeignKey(
        MailBox, on_delete=models.CASCADE, related_name="recipients"
    )
    name = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField()
    recipient_type = models.CharField(max_length=3, choices=RECIPIENT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.email} ({self.recipient_type})"
