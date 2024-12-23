import json
import secrets
import mimetypes
from django.http import QueryDict
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
            "created_at",
            "email_type",
            "is_starred",
            "recipients",
            "total_size",
            "attachments",
        ]
        read_only_fields = ["id", "total_size"]

    def run_validation(self, data):
        if isinstance(data, QueryDict):
            data = data.dict()

        if "recipients" in data and isinstance(data["recipients"], str):
            try:
                data["recipients"] = json.loads(data["recipients"])
                data["attachments"] = [
                    {"file": file} for file in self.initial_data.getlist("attachments")
                ]
            except json.JSONDecodeError:
                raise ValidationError({"recipients": "Invalid JSON format."})
        return super().run_validation(data)

    def validate(self, attrs):
        email_type = attrs.get("email_type")
        body = attrs.get("body", "").strip()
        subject = attrs.get("subject", "").strip()
        recipients = attrs.get("recipients", [])

        if email_type == Email.SENT:
            if not recipients or len(recipients) == 0:
                raise serializers.ValidationError(
                    {"recipients": "At least one recipient is required."}
                )

            if not body:
                raise serializers.ValidationError(
                    {"body": "The email body cannot be empty."}
                )

            if not subject:
                raise serializers.ValidationError(
                    {"subject": "The email subject cannot be empty."}
                )

        return super().validate(attrs)

    def create(self, validated_data):
        request = self.context.get("request")
        recipients_data = validated_data.pop("recipients", [])
        attachments_data = validated_data.pop("attachments", [])
        email_type = validated_data.get("email_type")

        if validated_data.get("is_seen"):
            del validated_data["is_seen"]

        if validated_data.get("is_starred"):
            del validated_data["is_starred"]

        if email_type not in (Email.DRAFT, Email.SENT):
            raise serializers.ValidationError(
                {"email_type": f"{email_type} is not a valid choice."}
            )

        email = Email.objects.create(
            **validated_data,
            primary_email_type=email_type,
            mailbox=request.mailbox,
            is_seen=True,
        )

        # Create attachments
        attachments = []
        size = 0
        for attachment in attachments_data:
            file = attachment.get("file")
            content_type, _ = mimetypes.guess_type(file.name)
            size += file.size
            attachments.append(
                EmailAttachment(
                    id=f"{EmailAttachment.UID_PREFIX}{secrets.token_hex(6)}",
                    mail=email,
                    filename=file.name.replace(" ", "_"),
                    content_type=content_type or "application/octet-stream",
                    file=file,
                )
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

        email.total_size = size
        email.save
        request.user.profile.add_size(size)
        EmailRecipient.objects.bulk_create(recipients)
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
