from rest_framework import serializers

from PasswordManager.models.folder import Folder
from PasswordManager.models.password import Password


class PasswordSerializer(serializers.ModelSerializer):
    folder = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all())
    file = serializers.FileField(write_only=True, required=False)
    file_type = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = Password
        fields = [
            "id",
            "url",
            "file",
            "notes",
            "title",
            "emoji",
            "folder",
            "username",
            "password",
            "file_name",
            "file_type",
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

    def get_file_name(self, obj):
        if obj.file:
            return obj.file.name.split("/")[-1]

    def get_file_type(self, obj):
        if obj.file:
            return "password-attachments"

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
