from django.db import models

from main.models.abstract.base import BaseModel


class EmailBox(BaseModel):
    INBOX = "inbox"
    SENT = "sent"
    DRAFT = "draft"
    TRASH = "trash"

    EMAIL_TYPE_CHOICES = [
        (SENT, "Sent"),
        (INBOX, "Inbox"),
        (DRAFT, "Draft"),
        (TRASH, "Trash"),
    ]
    email = models.ForeignKey(
        "NeuroMail.Email", on_delete=models.CASCADE, related_name="email_boxes"
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachment = models.FileField(upload_to="email_attachments/", null=True, blank=True)
    to = models.TextField(
        help_text="Comma-separated email addresses for 'To'", blank=True
    )
    cc = models.TextField(
        help_text="Comma-separated email addresses for 'CC'", blank=True
    )
    bcc = models.TextField(
        help_text="Comma-separated email addresses for 'BCC'", blank=True
    )
    email_type = models.CharField(
        max_length=10, choices=EMAIL_TYPE_CHOICES, default=INBOX
    )
    is_starred = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.email_type}"
