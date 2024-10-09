from rest_framework import exceptions
from rest_framework import serializers

from main.models.feature import Feature
from NeuroMail.models.email import Email
from NeuroMail.models.email_extension import EmailExtension
from NeuroMail.utils.mail_server_apis import create_mail_box
from main.utils.auth import generate_random_password


class EmailSerializer(serializers.ModelSerializer):
    local_part = serializers.CharField(write_only=True, required=True)
    domain = serializers.PrimaryKeyRelatedField(
        queryset=EmailExtension.objects.all(), write_only=True
    )

    class Meta:
        model = Email
        fields = [
            "id",
            "email",
            "domain",
            "local_part",
        ]
        read_only_fields = ["id", "email"]

    def validate(self, attrs):
        local_part = attrs.get("local_part")
        domain = attrs.get("domain")

        # Combine local_part and domain to form the full email
        email = f"{local_part}@{domain.name}"

        # Check if the email with this local_part and domain already exists
        if Email.objects.filter(email=email).exists():
            raise exceptions.ValidationError(
                {"email": "An email with this local part and domain already exists."}
            )

        attrs["email"] = email
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        domain = validated_data.pop("domain")
        password = generate_random_password()
        validated_data["password"] = password
        local_part = validated_data.pop("local_part")

        if self.context.get("is_check", False):
            # Return a response indicating that the email is available (doesn't exist)
            return {}

        # Check if the user has reached the email quota
        email_feature_value = Feature.get_feature_value(
            Feature.Code.NUMBER_OF_EMAILS, user
        )
        if user.emails.count() >= email_feature_value:
            raise exceptions.PermissionDenied(
                "Your email quota is full. Upgrade your subscription to create more emails."
            )

        success, msg = create_mail_box(local_part, password, domain.name)
        if success:
            return super().create(validated_data)
        raise serializers.ValidationError(msg)
