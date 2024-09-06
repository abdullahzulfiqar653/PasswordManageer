from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from api.utils import hash_passphrase


class UserSignInSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    pass_phrase = serializers.CharField(write_only=True)

    def create(self, validated_data):
        pass_phrase = validated_data["pass_phrase"]
        hash = hash_passphrase(pass_phrase)

        user = User.objects.filter(username=pass_phrase).first()
        if user and user.check_password(hash):
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        raise AuthenticationFailed("Invalid Seed.")
