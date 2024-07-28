import secrets
from rest_framework import serializers

from api.utils import generate_keypair
from api.models.keypair import KeyPair


class KeyPairSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = KeyPair
        fields = ["id", "name", "email", "private_key", "public_key"]
        read_only_fields = ["private_key", "public_key"]

    def create(self, validated_data):
        user = self.context["request"].user

        name = (
            f"pair_{secrets.token_hex(5)}"
            if not validated_data.get("name")
            else validated_data["name"]
        )

        # Generate key pairs
        private_key, public_key = generate_keypair()

        # Save the key pairs in the database
        key_pair = KeyPair.objects.create(
            user=user,
            name=name,
            private_key=private_key.decode("utf-8"),
            public_key=public_key.decode("utf-8"),
        )
        return key_pair
