import mimetypes

from rest_framework import serializers

from NeuroDrive.models import File
from NeuroDrive.models.directory import Directory

from main.services.s3 import S3Service
from main.utils.utils import get_file_metadata

s3_client = S3Service()


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        request = self.context.get("request")
        file = validated_data["file"]

        directory_id = self.context.get("directory_id")

        if not directory_id:
            raise serializers.ValidationError({"directory_id": "Missing directory ID"})

        try:
            directory = Directory.objects.get(id=directory_id)
        except Directory.DoesNotExist:
            raise serializers.ValidationError({"directory_id": "Invalid directory ID"})
        except ValueError:
            raise serializers.ValidationError(
                {"directory_id": "Invalid directory ID format"}
            )

        name = file.name.replace(" ", "_")
        content_type, _ = mimetypes.guess_type(file.name)

        s3_key = f"neurodrive/{directory.id}/{name}"
        s3_url = s3_client.upload_file(file, s3_key)

        file_instance = File.objects.create(
            name=name,
            s3_url=s3_url,
            size=file.size,
            owner=request.user,
            directory=directory,
            content_type=content_type or "application/octet-stream",
            metadata=get_file_metadata(file),
        )

        return file_instance
