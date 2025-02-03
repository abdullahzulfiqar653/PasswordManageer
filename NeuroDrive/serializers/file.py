import mimetypes

from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.contrib.auth.hashers import make_password, check_password

from main.services.s3 import S3Service
from NeuroDrive.models.file import File
from NeuroDrive.models.shared_access import SharedAccess

from main.utils.utils import get_file_metadata

s3_client = S3Service()


class FileSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True)
    file = serializers.FileField(required=False)
    metadata = serializers.JSONField(read_only=True)
    is_password_protected = serializers.SerializerMethodField()
    name = serializers.CharField(max_length=255, required=False)
    user_address = serializers.CharField(write_only=True, required=False)
    is_remove_metadata = serializers.BooleanField(default=False, write_only=True)
    is_remove_password = serializers.BooleanField(write_only=True, required=False)
    is_giving_permission = serializers.BooleanField(write_only=True, required=False, default=False )
    password = serializers.CharField( write_only=True, required=False, validators=[MinLengthValidator(8)])

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
            "user_address",
            "is_giving_permission",
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
        _ = validated_data.pop("is_giving_permission", None)
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
        is_giving_permission = validated_data.pop("is_giving_permission", False)
        user_address = validated_data.pop("user_address", None)
        is_remove_password = validated_data.pop("is_remove_password", False)

        if is_remove_password:
            if not password:
                raise serializers.ValidationError(
                    "Current password is required to remove password."
                )
            if instance.password is None:
                raise serializers.ValidationError("No password set for this file.")

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

        if is_giving_permission and user_address:
            try:
                user_to_share_with = User.objects.get(profile__address=user_address)

                SharedAccess.objects.create(
                    user=user_to_share_with,
                    item=instance,
                    permission_type=SharedAccess.Permission.FULL,
                )
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    f"User with address {user_address} not found."
                )

        if hasattr(request, "directory") and hasattr(request, "file"):
            validated_data["directory"] = request.directory

        return super().update(instance, validated_data)
