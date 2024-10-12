import secrets
from rest_framework.response import Response

from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend

from NeuroMail.models.email import Email
from NeuroMail.models.email_recipient import EmailRecipient

from NeuroMail.utils.imap_server import fetch_inbox_emails

from NeuroMail.serializers.email import EmailSerializer
from NeuroMail.serializers.email_trash import EmailTrashSerializer
from NeuroMail.serializers.email_starred import EmailUpdateSerializer
from NeuroMail.permissions import IsMailBoxOwner


class MailboxEmailListCreateView(generics.ListCreateAPIView):
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

            for email in emails:
                new_email = Email(
                    id=f"{Email.UID_PREFIX}{secrets.token_hex(6)}",
                    mailbox=mailbox,
                    body=email["body"],
                    is_seen=email["is_seen"],
                    subject=email["subject"],
                    email_type=email["email_type"],
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
            Email.objects.bulk_create(new_emails)
            EmailRecipient.objects.bulk_create(recipients)
        return mailbox.emails.all()


class MailboxEmailRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsMailBoxOwner]

    def get_serializer_class(self):
        if self.request.method in ("PATCH", "PUT"):
            return EmailUpdateSerializer
        return EmailSerializer

    def get_queryset(self):
        mailbox = self.request.mailbox
        return mailbox.emails.all()


class MailboxEmailMoveToTrashView(generics.UpdateAPIView):
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
