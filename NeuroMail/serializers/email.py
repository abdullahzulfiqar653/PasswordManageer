import secrets
import mimetypes
from rest_framework import serializers

from NeuroMail.utils.smtp_server import send_email

from NeuroMail.models.email import Email
from NeuroMail.models.email_recipient import EmailRecipient
from NeuroMail.models.email_attachment import EmailAttachment

from NeuroMail.serializers.email_recipient import EmailRecipientSerializer
from NeuroMail.serializers.email_attachment import EmailAttachmentSerializer


class EmailSerializer(serializers.ModelSerializer):
    recipients = EmailRecipientSerializer(many=True)
    attachments = EmailAttachmentSerializer(many=True)

    class Meta:
        model = Email
        fields = [
            "id",
            "body",
            "subject",
            "is_seen",
            "email_type",
            "is_starred",
            "recipients",
            "total_size",
            "attachments",
        ]
        read_only_fields = ["id", "total_size"]

    def create(self, validated_data):
        request = self.context.get("request")
        recipients_data = validated_data.pop("recipients", [])
        attachments_data = validated_data.pop("attachments", [])
        email_type = validated_data.get("email_type")
        if email_type not in (Email.DRAFT, Email.SENT):
            raise serializers.ValidationError(
                {"email_type": f"{email_type} is not a valid choice."}
            )

        email = Email.objects.create(
            **validated_data, primary_email_type=email_type, mailbox=request.mailbox
        )
        recipients = [
            EmailRecipient(
                id=f"{EmailRecipient.UID_PREFIX}{secrets.token_hex(6)}",
                mail=email,
                name=recipient_data.get("name", None),
                email=recipient_data["email"],
                recipient_type=recipient_data["recipient_type"],
            )
            for recipient_data in recipients_data
        ]
        EmailRecipient.objects.bulk_create(recipients)

        # Create attachments
        attachments = []
        for attachment in attachments_data:
            file = attachment.get("file")
            if file:
                # Identify content type and filename
                content_type, _ = mimetypes.guess_type(file.name)
                attachments.append(
                    EmailAttachment(
                        id=f"{EmailAttachment.UID_PREFIX}{secrets.token_hex(6)}",
                        email=email,
                        filename=file.name,
                        content_type=content_type or "application/octet-stream",
                        file=file,
                    )
                )
        EmailAttachment.objects.bulk_create(attachments)

        if email_type == Email.SENT:
            send_email(
                validated_data["subject"],
                validated_data["body"],
                request.mailbox.email,
                request.mailbox.password,
                recipients_data,
                [attachment.file.path for attachment in attachments],
            )
        return email
