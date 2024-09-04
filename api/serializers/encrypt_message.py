from rest_framework import serializers
from api.models.recipient import Recipient
from api.utils import encrypt_messages


class EncryptMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    recipient_ids = serializers.ListField(write_only=True)

    def validate_recipient_ids(self, recipient_ids):
        if not recipient_ids:
            raise serializers.ValidationError("At least one Recipient required.")
        user = self.context["request"].user
        invalid_ids = (
            Recipient.objects.filter(id__in=recipient_ids)
            .exclude(user=user)
            .values_list("id", flat=True)
        )
        if invalid_ids:
            raise serializers.ValidationError(
                f"These {list(invalid_ids)} IDs in the list are not related to the current user."
            )
        return recipient_ids

    def validate_message(self, message):
        if len(message) > 446:
            raise serializers.ValidationError(
                "Message content cannot be greater then 446 characters."
            )
        return message

    def create(self, validated_data):
        message = validated_data.get("message").encode()
        recipient_ids = validated_data.get("recipient_ids")

        encrypted_message = encrypt_messages(
            message,
            [
                recipient.public_key
                for recipient in Recipient.objects.filter(id__in=recipient_ids)
            ],
        )
        return {"message": encrypted_message}
