from rest_framework import serializers
from api.models.keypair import KeyPair
from api.utils import decrypt_message


class DecryptMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    keypair_id = serializers.CharField(write_only=True)

    def validate_keypair_id(self, keypair_id):
        user = self.context["request"].user
        if not KeyPair.objects.filter(id=keypair_id, user=user).exists():
            raise serializers.ValidationError("Keypair does not exist.")
        return keypair_id

    def create(self, validated_data):
        encrypted_message = bytes.fromhex(validated_data.get("message"))
        keypair_id = validated_data.get("keypair_id")

        # Get the private key from the KeyPair model
        keypair = KeyPair.objects.get(id=keypair_id)
        private_key_pem = keypair.private_key.encode("utf-8")

        # Decrypt the message
        decrypted_message = decrypt_message(encrypted_message, private_key_pem)

        return {"message": decrypted_message.decode()}
