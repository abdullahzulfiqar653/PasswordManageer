import os
from rest_framework import serializers

from main.models.feature import Feature
from main.models.user_profile import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    features_data = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["id", "image", "features_data"]

    def get_features_data(self, obj):
        request = self.context.get("request")
        return {
            "total_size": round(obj.total_size / (1024**3), 2),
            "size_allowed": Feature.get_feature_value(
                Feature.Code.STORAGE_GB, request.user
            ),
            "total_mailbox": request.user.mailboxes.count(),
            "mailbox_allowed": Feature.get_feature_value(
                Feature.Code.NUMBER_OF_MAILBOX, request.user
            ),
        }

    def update(self, instance, validated_data):
        if validated_data.get("image", None) and instance.image:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
        return super().update(instance, validated_data)
