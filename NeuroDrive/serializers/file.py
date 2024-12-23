import mimetypes
from rest_framework import serializers

from NeuroDrive.models.file import File


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = [
            "id",
            "name",
            "file",
            "size",
            "directory",
            "is_starred",
            "content_type",
        ]
        read_only_fields = ["size", "directory", "content_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        file = validated_data.get("file")
        request = self.context.get("request")
        content_type, _ = mimetypes.guess_type(file.name)

        validated_data["size"] = file.size
        validated_data["owner"] = request.user
        validated_data["directory"] = request.directory
        validated_data["content_type"] = content_type or "application/octet-stream"

        if validated_data.get("is_starred"):
            del validated_data["is_starred"]

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # todo
        # on update of name update file name
        return super().update(instance, validated_data)
