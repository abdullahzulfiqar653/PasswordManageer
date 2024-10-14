from rest_framework import serializers
from NeuroMail.models import EmailAttachment


class EmailAttachmentSerializer(serializers.ModelSerializer):
    file_type = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True)  # Make file write-only

    class Meta:
        model = EmailAttachment
        fields = ["id", "filename", "content_type", "file", "file_type"]
        read_only_fields = ["id", "filename", "content_type"]

    def get_file_type(self, obj):
        return "mailbox-attachments"
