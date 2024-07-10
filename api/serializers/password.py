from rest_framework import serializers
from api.models.password import Password
from rest_framework import exceptions


class PasswordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = "__all__"

    def validate_user(self, user):
        if user.id != self.context["request"].user.id:
            raise exceptions.PermissionDenied(
                "Permission denied: User ID in payload does not match request user ID."
            )
        return user
