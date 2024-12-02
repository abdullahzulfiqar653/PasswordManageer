from rest_framework import exceptions
from rest_framework import serializers

from main.models.feature import Feature
from NeuroMail.models.mailbox import MailBox
from NeuroMail.models.email_extension import EmailExtension
from NeuroMail.utils.mail_server_apis import create_mail_box, validate_mailbox
from main.utils.auth import generate_random_password


class MailboxSerializer(serializers.ModelSerializer):
    local_part = serializers.CharField(write_only=True, required=True)
    domain = serializers.PrimaryKeyRelatedField(
        queryset=EmailExtension.objects.all(), write_only=True
    )

    class Meta:
        model = MailBox
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
        email = f"{local_part}@{domain.name}"

        success, msg = validate_mailbox(email)
        if not success:
            raise exceptions.ValidationError(msg)

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
        mailbox_allowed = Feature.get_feature_value(
            Feature.Code.NUMBER_OF_MAILBOX, user
        )
        if user.mailboxes.count() >= mailbox_allowed:
            raise exceptions.PermissionDenied(
                {
                    "error": [
                        "Your mailboxes quota is full. Upgrade your subscription to create more mailboxes."
                    ]
                }
            )

        success, msg = create_mail_box(local_part, password, domain.name)
        if success:
            return super().create(validated_data)
        raise serializers.ValidationError(msg)
