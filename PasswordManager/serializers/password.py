from rest_framework import serializers

from PasswordManager.models.folder import Folder
from PasswordManager.models.password import Password


class PasswordSerializer(serializers.ModelSerializer):
    folder = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all())

    class Meta:
        model = Password
        fields = [
            "id",
            "url",
            "notes",
            "title",
            "emoji",
            "folder",
            "username",
            "password",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]

    def __init__(self, *args, **kwargs):
        """
        Modifying the queryset of the folders field based on the request user.
        """
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if hasattr(request, "user") and request.user.is_authenticated:
            self.fields["folder"].queryset = request.user.folders.all()

    def validate(self, attrs):
        user = self.context["request"].user
        check = {key: attrs.get(key, None) for key in ["url", "title", "username"]}
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
