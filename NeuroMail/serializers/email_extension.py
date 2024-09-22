from rest_framework import serializers

from NeuroMail.models.email_extension import EmailExtension


class EmailExtensionSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailExtension
        fields = "__all__"
