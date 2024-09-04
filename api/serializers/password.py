from rest_framework import serializers
from api.models.password import Password
from rest_framework import exceptions


class PasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Password
        fields = [
            "id",
            "url",
            "notes",
            "title",
            "emoji",
            "username",
            "password",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]

    def validate(self, attrs):
        user = self.context["request"].user
        check = {key: attrs[key] for key in ["url", "title", "username"]}
        if not self.instance:
            if user.passwords.filter(**check).exists():
                raise serializers.ValidationError(
                    {
                        "error": "An entry with this title, username, and URL already exists."
                    }
                )
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
