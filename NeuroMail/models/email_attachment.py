from django.db import models
from NeuroMail.models.email import Email
from main.models.abstract.base import BaseModel


class EmailAttachment(BaseModel):
    UID_PREFIX = 125
    mail = models.ForeignKey(
        Email, on_delete=models.CASCADE, related_name="attachments"
    )
    filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    file = models.FileField(upload_to="protected/mailbox/attachments/")

    def __str__(self):
        return f"Attachment for {self.mail.subject} ({self.filename})"
