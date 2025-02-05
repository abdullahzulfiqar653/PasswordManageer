from rest_framework import serializers
from NeuroDrive.models.shared_access import SharedAccess
from main.services.s3 import S3Service

client = S3Service()


class SharedAccessSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = SharedAccess
        fields = ["id", "image"]

    def get_image(self, obj):
        user_profile = getattr(obj.user, "profile", None)
        if user_profile and user_profile.image_name:
            return client.generate_presigned_url(user_profile.image_name)
        return None
