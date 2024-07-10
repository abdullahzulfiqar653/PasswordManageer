from rest_framework import serializers
from django.contrib.auth.models import User
from api.utils import generate_passphrase, hash_passphrase


class UserSignUpSerializer(serializers.Serializer):
    pass_phrase = serializers.CharField(read_only=True)
    phrase_length = serializers.IntegerField(write_only=True, default=6)

    def create(self, validated_data):
        passphrase = generate_passphrase(validated_data["phrase_length"])
        hashed_passphrase = hash_passphrase(passphrase)
        while User.objects.filter(username=passphrase).exists():
            passphrase = generate_passphrase()
            hashed_passphrase = hash_passphrase(passphrase)
        user = User.objects.create(username=passphrase)
        user.set_password(hashed_passphrase)
        user.save()
        return {"pass_phrase": passphrase}
