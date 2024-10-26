from rest_framework import serializers
from NeuroRsa.models.recipient import Recipient


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ["id", "name", "public_key", "emoji"]

    def validate(self, attrs):
        user = self.context["request"].user
        queryset = Recipient.objects.filter(user=user, name=attrs.get("name"))
        if self.isinstance:
            queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise serializers.ValidationError("Recipient with this name already exists")

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
