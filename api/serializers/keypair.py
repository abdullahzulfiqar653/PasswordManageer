import secrets
from rest_framework import serializers

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
                "An entry with this user and name already exists."
            )
        return name

    def create(self, validated_data):
        user = self.context["request"].user

        email = validated_data.get("email")
        # Convert passphrase to bytes if present, otherwise None
        passphrase = validated_data.get("passphrase")
        passphrase_bytes = passphrase.encode("utf-8") if passphrase else None

        name = (
            f"pair_{secrets.token_hex(3)}"
            if not validated_data.get("name")
            else validated_data["name"]
        )

        # Generate key pairs
        private_key, public_key = generate_keypair(passphrase_bytes)

        # Save the key pairs in the database
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
