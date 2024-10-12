from rest_framework import serializers
from NeuroMail.models.email_recipient import EmailRecipient


class EmailRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailRecipient
        fields = ["id", "mail", "email", "recipient_type", "name"]
        read_only_fields = ["id", "mail"]
