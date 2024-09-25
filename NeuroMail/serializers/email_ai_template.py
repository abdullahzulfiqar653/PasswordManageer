from rest_framework import serializers

from NeuroMail.models.email_ai_template import EmailAiTemplate


class EmailAiTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailAiTemplate
        fields = "__all__"
