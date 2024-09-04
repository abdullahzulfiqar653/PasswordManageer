import secrets

from rest_framework import serializers
from django.contrib.auth.models import User

from api.utils import hash_passphrase
from api.utils import generate_keypair
from api.models.keypair import KeyPair


class KeyPairSerializer(serializers.ModelSerializer):
    passphrase = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        allow_null=True,
        max_length=64,
    )

    class Meta:
        model = KeyPair
        fields = ["id", "name", "email", "passphrase", "private_key", "public_key"]
        read_only_fields = ["private_key", "public_key"]

    def validate_name(self, name):
        user = self.context.get("request").user
        if KeyPair.objects.filter(user_id=user, name=name).exists():
            raise serializers.ValidationError(
                "An keypair with this user and name already exists."
            )
        return name

    def create(self, validated_data):
        user = self.context["request"].user

        email = validated_data.get("email")
        passphrase = validated_data.get("passphrase")
        passphrase_bytes = passphrase.encode("utf-8") if passphrase else None

        name = validated_data.get("name") or f"pair_{secrets.token_hex(3)}"
        private_key, public_key = generate_keypair(passphrase_bytes)

        key_pair = KeyPair.objects.create(
            user=user,
            name=name,
            email=email,
            passphrase=passphrase,
            private_key=private_key.decode("utf-8"),
            public_key=public_key.decode("utf-8"),
        )
        return key_pair

    def update(self, instance, validated_data):
        validated_data.pop("passphrase", None)
        return super().update(instance, validated_data)


class MainKeyPairSerializer(serializers.Serializer):
    """
    This Serializer is used to create a main keypair for every user in this
    application or for the users of other applicatiuons as well.
    """

    private_key = serializers.CharField(read_only=True)
    public_key = serializers.CharField(read_only=True)
    pass_phrase = serializers.CharField(write_only=True)

    def validate(self, attrs):
        pass_phrase = attrs.get("pass_phrase")
        if User.objects.filter(username=pass_phrase).exists():
            raise serializers.ValidationError(
                {"msg": "User already have main keypair."}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        pass_phrase = validated_data["pass_phrase"]
        hash = hash_passphrase(pass_phrase)
        user, _ = User.objects.get_or_create(username=pass_phrase)
        user.set_password(hash)
        user.save()
        
        private_key, public_key = generate_keypair()
        KeyPair.objects.create(
            user=user,
            is_main=True,
            name=f"main_{secrets.token_hex(3)}",
            public_key=public_key.decode("utf-8"),
            private_key=private_key.decode("utf-8"),
        )
        return {
            "public_key": public_key.decode("utf-8"),
            "private_key": private_key.decode("utf-8"),
        }
