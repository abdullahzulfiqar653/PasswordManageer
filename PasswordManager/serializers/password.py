import mimetypes
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
            "content_type",
        ]
        read_only_fields = ["updated_at", "content_type"]

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

    def validate_title(self, value):
        user = self.context["request"].user
        queryset = user.passwords.filter(title=value)
        error = serializers.ValidationError(
            {"title": "An entry with this title already exists. "}
        )
        if self.instance:
            if queryset.exclude(title=value).exist():
                raise error
        else:
            if queryset.exists():
                raise error
        return value

    def create(self, validated_data):
        file = validated_data.get("file", None)
        if file:
            validated_data["content_type"] = (
                file.content_type or mimetypes.guess_type(file.name)[0]
            )
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        file = validated_data.get("file", None)
        if file:
            validated_data["content_type"] = (
                file.content_type or mimetypes.guess_type(file.name)[0]
            )
        else:
            validated_data["file"] = instance.file
        return super().update(instance, validated_data)
