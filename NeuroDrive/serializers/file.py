import mimetypes
from rest_framework import serializers
from main.services.s3 import S3Service
from NeuroDrive.models.file import File
from main.utils.utils import get_file_metadata


class FileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False)
    file = serializers.FileField(required=False)
    url = serializers.URLField(read_only=True)
    metadata = serializers.JSONField(read_only=True)
    is_removed_metadata = serializers.BooleanField(default=False, write_only=True)
    
    class Meta:
        model = File
        fields = [
            "id",
            "url",
            "name",
            "file",
            "size",
            "directory",
            "metadata",
            "content_type",
            "is_removed_metadata"
        ]
        read_only_fields = ["size", "directory", "content_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
            raise serializers.ValidationError(
                {
                    "error": [
                        "A file with the same name already exists in this directory for this owner."
                    ]
                }
            )
        return data

    def create(self, validated_data):
        validated_data.pop("is_removed_metadata", None)
        file = validated_data.pop("file")
        request = self.context.get("request")
        name = validated_data.get("name", file.name).replace(" ", "_")
        content_type, _ = mimetypes.guess_type(file.name)
        s3_client = S3Service()
        s3_key = f"neurodrive/{request.directory.id}/{name}"
        s3_url = s3_client.upload_file(file, s3_key)
        validated_data["name"] = name
        validated_data["s3_url"] = s3_url
        validated_data["size"] = file.size
        validated_data["owner"] = request.user
        validated_data["directory"] = request.directory
        validated_data["content_type"] = content_type or "application/octet-stream"
        validated_data["metadata"] = get_file_metadata(file, content_type)
    
        if validated_data.get("is_starred"):
            del validated_data["is_starred"]

        return super().create(validated_data)

    def update(self, instance, validated_data):
        is_removed_metadata = validated_data.pop("is_removed_metadata", False)
        request = self.context.get("request")
        if is_removed_metadata:
            instance.metadata = {}
        if hasattr(request, "directory") and hasattr(request, "file"):
            validated_data["directory"] = request.directory
        return super().update(instance, validated_data)
