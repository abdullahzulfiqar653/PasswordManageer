from rest_framework import serializers

from main.services.s3 import S3Service

from main.models.feature import Feature
from main.models.user_profile import UserProfile

client = S3Service()


class UserProfileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    features_data = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "image", "features_data", "url"]

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

    def get_url(self, obj):
        if obj.image_name:
            return client.generate_presigned_url(obj.image_name, 604800)

    def update(self, instance, validated_data):
        image = validated_data.get("image", None)
        profile_id = self.context.get("request").user.profile.id

        if image:
            image_key = f"profile/{profile_id}/{image.name.replace(' ', '_')}"
            s3_url = client.upload_file(image, image_key)
            validated_data["image_name"] = s3_url
        return super().update(instance, validated_data)
