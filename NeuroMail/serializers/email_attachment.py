from rest_framework import serializers
from main.services.s3 import S3Service
from NeuroMail.models import EmailAttachment


class EmailAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)  # Make file write-only

    class Meta:
        model = EmailAttachment
        fields = ["id", "filename", "content_type", "file"]
        read_only_fields = ["id", "filename", "content_type"]
