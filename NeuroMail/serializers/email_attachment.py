from rest_framework import serializers
from NeuroMail.models import EmailAttachment


class EmailAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAttachment
        fields = ["id", "filename", "content_type", "file"]
        read_only_fields = ["id", "filename", "content_type"]
