import secrets
from rest_framework import serializers

from NeuroMail.models.email import Email
from NeuroMail.models.mailbox import MailBox
from NeuroMail.models.mailbox_recipient import MailBoxRecipient

from NeuroMail.utils.smtp_server import send_email
from NeuroMail.serializers.mailbox_recipient import MailBoxEmailRecipientSerializer


class MailBoxSerializer(serializers.ModelSerializer):
    email = serializers.PrimaryKeyRelatedField(queryset=Email.objects.none())
    recipients = MailBoxEmailRecipientSerializer(many=True)

    class Meta:
        model = MailBox
        fields = [
            "id",
            "body",
            "email",
            "subject",
            "attachment",
            "email_type",
            "is_starred",
            "recipients",
        ]
        read_only_fields = ["id"]

    def __init__(self, *args, **kwargs):
        """
        Modifying the queryset of the email field based on the request user.
        """
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if hasattr(request, "user") and request.user.is_authenticated:
            self.fields["email"].queryset = request.user.emails.all()

    def create(self, validated_data):
        email = validated_data.get("email")
        recipients_data = validated_data.pop("recipients")
        email_type = validated_data.get("email_type")
        if email_type not in (MailBox.DRAFT, MailBox.SENT):
            raise serializers.ValidationError(
                {"email_type": f"{email_type} is not a valid choice."}
            )
        mail_box = MailBox.objects.create(
            **validated_data, primary_email_type=email_type
        )
        recipients = [
            MailBoxRecipient(
                id=f"{MailBox.UID_PREFIX}{secrets.token_hex(5)}",
                mail_box=mail_box,
                email=recipient_data["email"],
                recipient_type=recipient_data["recipient_type"],
            )
            for recipient_data in recipients_data
        ]
        MailBoxRecipient.objects.bulk_create(recipients)
        if email_type == MailBox.SENT:
            send_email(
                validated_data["subject"],
                validated_data["body"],
                email.email,
                email.password,
                recipients_data,
            )
        return mail_box
