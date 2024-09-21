from rest_framework import exceptions
from rest_framework import serializers

from NeuroMail.models.email import Email
from main.models.feature import Feature


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = [
            "id",
            "email",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        email_feature_value = Feature.get_feature_value(
            Feature.Code.NUMBER_OF_EMAILS, user
        )
        print(email_feature_value)
        if user.emails.count() >= email_feature_value:
            raise exceptions.PermissionDenied(
                "Your email quota is full. Upgrade your subscription to create more emails."
            )
        validated_data["user"] = user
        return super().create(validated_data)
