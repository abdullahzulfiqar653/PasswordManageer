from rest_framework import serializers
from api.models.keypair import KeyPair
from api.utils import decrypt_message


def get_passphrase(passphrase, keypair):
    if not keypair.passphrase:
        return
    return passphrase.encode("utf-8")


class DecryptMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    keypair_id = serializers.CharField(write_only=True)
    passphrase = serializers.CharField(max_length=64, write_only=True, allow_null=True)

    def validate(self, data):
        keypair_id = data.get("keypair_id")
        passphrase = data.get("passphrase")
        user = self.context["request"].user

        if not KeyPair.objects.filter(id=keypair_id, user=user).exists():
            raise serializers.ValidationError({"keypair_id": "Keypair does not exist."})

        keypair = KeyPair.objects.get(id=keypair_id, user=user)
        if not keypair.passphrase:
            return data

        if not passphrase:
            raise serializers.ValidationError(
                {
                    "passphrase": "Your keypair is encrypted with a passphrase. Please provide it to use the keypair."
                }
            )

        if not KeyPair.objects.filter(id=keypair.id, passphrase=passphrase).exists():
            raise serializers.ValidationError(
                {"passphrase": "Invalid passphrase. Please try again."}
            )
        return data

    def create(self, validated_data):
        encrypted_message_strings = [
            bytes.fromhex(hs) for hs in validated_data.get("message").split("-") if hs
        ]
        keypair = KeyPair.objects.get(id=validated_data.get("keypair_id"))
        passphrase = get_passphrase(validated_data.get("passphrase"), keypair)

        # Get the private key from the KeyPair model
        private_key_pem = keypair.private_key.encode("utf-8")

        # Decrypt the message
        decrypted_message = decrypt_message(
            encrypted_message_strings, private_key_pem, passphrase
        )
        if not decrypted_message:
            raise serializers.ValidationError(
                {"keypair": "Decryption failed: Invalid keypair selected."}
            )
        return {"message": decrypted_message.decode()}
