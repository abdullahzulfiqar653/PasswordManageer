import secrets

from rest_framework import generics, status
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django_filters.rest_framework import DjangoFilterBackend

from NeuroMail.models.email import Email
from NeuroMail.models.mailbox import MailBox
from NeuroMail.models.email_recipient import EmailRecipient
from NeuroMail.models.email_attachment import EmailAttachment


from NeuroMail.serializers.email import EmailSerializer
from NeuroMail.serializers.email_trash import EmailTrashSerializer
from NeuroMail.serializers.email_starred import EmailUpdateSerializer

from NeuroMail.permissions import IsMailBoxOwner
from NeuroMail.utils.imap_server import fetch_inbox_emails


class MailboxEmailListCreateView(generics.ListCreateAPIView):
    """THis API used to create emails of type [sent, draft] and use to list emails of all types"""

    queryset = Email.objects.none()
    serializer_class = EmailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["email_type", "is_starred", "is_seen"]
    permission_classes = [IsMailBoxOwner]

    def get_queryset(self):
        mailbox = self.request.mailbox
        email_type = self.request.query_params.get("email_type")
        if email_type == Email.INBOX:
            emails = fetch_inbox_emails(mailbox.email, mailbox.password)
            new_emails = []
            recipients = []
            attachments = []
            total_emails_size = 0
            for email in emails:
                total_size = len(email["body"].encode("utf-8"))  # Size of body in bytes
                new_email = Email(
                    id=f"{Email.UID_PREFIX}{secrets.token_hex(6)}",
                    mailbox=mailbox,
                    body=email["body"],
                    is_seen=email["is_seen"],
                    subject=email["subject"],
                    email_type=email["email_type"],
                    primary_email_type=email["email_type"],
                )
                new_emails.append(new_email)
                for recipient in email["recipients"]:
                    recipients.append(
                        EmailRecipient(
                            id=f"{EmailRecipient.UID_PREFIX}{secrets.token_hex(6)}",
                            mail=new_email,
                            **recipient,
                        )
                    )
                # Create attachments
                for attachment in email.get("attachments", []):
                    attachment_size = len(attachment["data"])
                    total_size += attachment_size
                    attachments.append(
                        EmailAttachment(
                            id=f"{EmailAttachment.UID_PREFIX}{secrets.token_hex(6)}",
                            mail=new_email,
                            filename=attachment["filename"],
                            content_type=attachment["content_type"],
                            file=ContentFile(
                                attachment["data"], name=attachment["filename"]
                            ),
                        )
                    )
                new_email.total_size = total_size
                total_emails_size += total_size
            self.request.user.profile.add_size(total_emails_size)
            Email.objects.bulk_create(new_emails)
            EmailRecipient.objects.bulk_create(recipients)
            EmailAttachment.objects.bulk_create(attachments)
        return mailbox.emails.all().order_by("-created_at")


class MailboxEmailRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """THis API use to fetch signle email data or to mark it as starred or seen"""

    permission_classes = [IsMailBoxOwner]

    def get_serializer_class(self):
        if self.request.method in ("PATCH", "PUT"):
            return EmailUpdateSerializer
        return EmailSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return MailBox.objects.none()
        mailbox = self.request.mailbox
        return mailbox.emails.all()


class MailboxEmailMoveToTrashView(generics.UpdateAPIView):
    """APIs to move emails to trash by sending list of email ids"""

    serializer_class = EmailTrashSerializer
    permission_classes = [IsMailBoxOwner]

    def update(self, request, *args, **kwargs):
        mailbox = self.request.mailbox
        serializer = self.get_serializer(
            data=request.data, context={"request": request, "mailbox": mailbox}
        )

        if serializer.is_valid():
            serializer.update_emails_to_trash()
            return Response(
                {"message": "Emails moved to trash successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MailboxEmailRestoreFromTrashView(generics.UpdateAPIView):
    """APIs to restore emails from trash by sending list of email ids"""

    serializer_class = EmailTrashSerializer
    permission_classes = [IsMailBoxOwner]

    def update(self, request, *args, **kwargs):
        mailbox = self.request.mailbox
        serializer = self.get_serializer(
            data=request.data, context={"request": request, "mailbox": mailbox}
        )

        if serializer.is_valid():
            serializer.update_trash_to_emails()
            return Response(
                {"message": "Emails restored from trash successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
