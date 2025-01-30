import mimetypes

from rest_framework import serializers
from django.core.validators import MinLengthValidator
from django.contrib.auth.hashers import make_password, check_password

from main.services.s3 import S3Service
from NeuroDrive.models.file import File
from main.utils.utils import get_file_metadata

s3_client = S3Service()


class FileSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True)
    file = serializers.FileField(required=False)
    metadata = serializers.JSONField(read_only=True)
    is_password_protected = serializers.SerializerMethodField()
    name = serializers.CharField(max_length=255, required=False)
    is_remove_password = serializers.BooleanField(write_only=True, required=False)
    is_remove_metadata = serializers.BooleanField(default=False, write_only=True)
    password = serializers.CharField(
        write_only=True, required=False, validators=[MinLengthValidator(8)]
    )

    class Meta:
        model = File
        fields = [
            "id",
            "url",
            "name",
            "file",
            "size",
            "metadata",
            "password",
            "directory",
            "is_starred",
            "content_type",
            "is_remove_metadata",
            "is_remove_password",
            "is_password_protected",
        ]
        read_only_fields = ["size", "directory", "content_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_is_password_protected(self, obj):
        """Check if the file is password protected"""
        return bool(obj.password)

    def validate(self, data):
        """
        Ensure that the combination of 'owner', 'name', and 'directory' is unique.
        """
        file = data.get("file", None)
        if not self.instance:
            if not file:
                raise serializers.ValidationError({"file": ["File is required"]})
        name = data.get("name", "")
        if not name:
            name = self.instance.name if self.instance else file.name
        request = self.context.get("request")

        query = File.objects.all()
        if self.instance:
            query = query.exclude(owner=request.user, directory=request.directory)
        if query.filter(
            owner=request.user, name=name, directory=request.directory
        ).exists():
            pass
        return data

    def create(self, validated_data):
        _ = validated_data.pop("is_starred", None)
        _ = validated_data.pop("is_remove_password", None)
        _ = validated_data.pop("is_remove_metadata", None)
        file = validated_data.pop("file")
        request = self.context.get("request")
        name = validated_data.get("name", file.name).replace(" ", "_")
        content_type, _ = mimetypes.guess_type(file.name)
        s3_key = f"neurodrive/{request.directory.id}/{name}"
        s3_url = s3_client.upload_file(file, s3_key)
        validated_data["name"] = name
        validated_data["s3_url"] = s3_url
        validated_data["size"] = file.size
        validated_data["owner"] = request.user
        validated_data["directory"] = request.directory
        validated_data["content_type"] = content_type or "application/octet-stream"
        validated_data["metadata"] = get_file_metadata(file)

        if validated_data.get("is_starred"):
            del validated_data["is_starred"]

        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        password = validated_data.pop("password", None)
        is_remove_password = validated_data.pop("is_remove_password", False)

        if is_remove_password:
            if not password:
                raise serializers.ValidationError(
                    "Current password is required to remove password."
                )

            if not check_password(password, instance.password):
                raise serializers.ValidationError("Incorrect password.")

            instance.password = None

        elif password:
            instance.password = make_password(password)

        is_remove_metadata = validated_data.pop("is_remove_metadata", False)
        if is_remove_metadata:
            instance.metadata = {}

        file = validated_data.pop("file", None)
        if file:
            name = validated_data.get("name", file.name).replace(" ", "_")
            content_type, _ = mimetypes.guess_type(file.name)
            s3_key = f"neurodrive/{request.directory.id}/{name}"
            s3_url = s3_client.upload_file(file, s3_key)
            validated_data["s3_url"] = s3_url
            validated_data["size"] = file.size
            validated_data["content_type"] = content_type or "application/octet-stream"

        if hasattr(request, "directory") and hasattr(request, "file"):
            validated_data["directory"] = request.directory
        return super().update(instance, validated_data)


class FileAccessSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    url = serializers.CharField(read_only=True)