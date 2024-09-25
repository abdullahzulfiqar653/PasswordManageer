from rest_framework import serializers
from NeuroRsa.models.recipient import Recipient
from NeuroRsa.utils import encrypt_message


class EncryptMessageSerializer(serializers.Serializer):
    message = serializers.CharField(allow_blank=True)
    recipient_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Recipient.objects.all(),
        write_only=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if getattr(request, "user", None):
            if getattr(request.user, "recipients", None):
                self.fields["recipient_ids"].queryset = request.user.recipients.all()

    def validate_recipient_ids(self, recipient_ids):
        if not recipient_ids:
            raise serializers.ValidationError("At least one Recipient required.")
        return recipient_ids

    def validate_message(self, message):
        if not message:
            raise serializers.ValidationError("Message content cannot be empty.")
        if len(message) > 446:
            raise serializers.ValidationError(
                "Message content cannot be greater then 446 characters."
            )
        return message

    def create(self, validated_data):
        message = validated_data.get("message").encode()
        recipients = validated_data.get("recipient_ids")
        try:
            encrypted_message = encrypt_message(
                message,
                [
                    recipient.public_key
                    for recipient in Recipient.objects.filter(
                        id__in=[recipients.id for recipients in recipients]
                    )
                ],
            )
        except Exception as e:  # noqa
            raise serializers.ValidationError(
                {
                    "error": [
                        f"{'Some of Recipients' if len(recipients) > 1 else 'Recipient'} has the wrong public key, which cannot be used to encrypt the message."
                    ]
                }
            )
        return {"message": encrypted_message}
