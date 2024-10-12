import secrets
from rest_framework import serializers

from NeuroMail.models.email import Email
from NeuroMail.models.email_recipient import EmailRecipient

from NeuroMail.utils.smtp_server import send_email
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
            "attachments",
            "email_type",
            "is_starred",
            "recipients",
            "total_size",
        ]
        read_only_fields = ["id", "total_size"]

    def create(self, validated_data):
        request = self.context.get("request")
        recipients_data = validated_data.pop("recipients")
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
                name=recipient_data["name"],
                email=recipient_data["email"],
                recipient_type=recipient_data["recipient_type"],
            )
            for recipient_data in recipients_data
        ]
        EmailRecipient.objects.bulk_create(recipients)
        if email_type == Email.SENT:
            send_email(
                validated_data["subject"],
                validated_data["body"],
                request.mailbox.email,
                request.mailbox.password,
                recipients_data,
            )
        return email
