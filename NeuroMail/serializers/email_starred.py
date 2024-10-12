from rest_framework import serializers
from NeuroMail.models.email import Email


class EmailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["is_starred", "is_seen"]
