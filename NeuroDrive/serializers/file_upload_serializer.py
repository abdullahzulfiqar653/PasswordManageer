from rest_framework import serializers


class FileFakeSerializer(serializers.Serializer):
    file = serializers.FileField()

