from rest_framework import serializers
from NeuroMail.models.mailbox_recipient import MailBoxRecipient


class MailBoxEmailRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailBoxRecipient
        fields = ["id", "mail_box", "email", "recipient_type", "name"]
        read_only_fields = ["id", "mail_box"]
