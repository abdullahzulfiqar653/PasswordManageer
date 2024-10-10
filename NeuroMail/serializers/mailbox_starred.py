from rest_framework import serializers
from NeuroMail.models.mailbox import MailBox


class MailboxStarredSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailBox
        fields = ["is_starred"]
