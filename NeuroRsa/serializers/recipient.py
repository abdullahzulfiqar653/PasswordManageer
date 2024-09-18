from rest_framework import serializers
from NeuroRsa.models.recipient import Recipient


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ["id", "name", "public_key"]

    def validate(self, attrs):
        user = self.context["request"].user
        if Recipient.objects.filter(
            user=user, name=attrs.get("name"), public_key=attrs.get("public_key")
        ).exists():
            raise serializers.ValidationError(
                "A recipient with this key pair name and public key already exists for this user."
            )

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
