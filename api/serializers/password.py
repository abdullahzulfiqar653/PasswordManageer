from rest_framework import serializers
from api.models.password import Password
from rest_framework import exceptions


class PasswordCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Password
        fields = ["id", "title", "username", "password", "url", "notes", "emoji"]
        # read_only_fields = ["user"]

    def validate(self, attrs):
        user = self.context["request"].user
        if user.passwords.filter(
            title=attrs["title"],
            username=attrs["username"],
            url=attrs.get("url"),
        ).exists():
            raise serializers.ValidationError(
                {"error": "An entry with this title, username, and URL already exists."}
            )
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
