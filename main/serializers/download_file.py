from rest_framework import serializers


class FileDownloadSerializer(serializers.Serializer):
    url = serializers.URLField(write_only=True)
