import os
from rest_framework import serializers

from main.models.user_profile import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "image", "total_size"]

    def update(self, instance, validated_data):
        if validated_data.get("image", None) and instance.image:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
        return super().update(instance, validated_data)
