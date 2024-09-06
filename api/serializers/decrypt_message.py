from rest_framework import serializers
from api.models.keypair import KeyPair
from api.utils import decrypt_message


def get_passphrase(passphrase, keypair):
    if not keypair.passphrase:
        return
    return passphrase.encode("utf-8")


class DecryptMessageSerializer(serializers.Serializer):
    message = serializers.CharField(allow_blank=True)
    keypair_id = serializers.CharField(write_only=True, allow_blank=True)
    passphrase = serializers.CharField(
        max_length=64, write_only=True, allow_null=True, allow_blank=True
    )

    def validate_keypair_id(self, value):
        if not value:
            raise serializers.ValidationError(
                "Choose a keypair to decrypt your message."
            )
        return value

    def validate_message(self, value):
        if not value:
            raise serializers.ValidationError("Message is required.")
        try:
            encrypted_message = (
                value.replace("-----BEGIN PGP MESSAGE BLOCK-----\n", "")
                .replace("\n-----END PGP MESSAGE BLOCK-----", "")
                .replace("\n", "")
            )
            encrypted_messages = [
                bytes.fromhex(hs) for hs in encrypted_message.split("-") if hs
            ]
        except:
            raise serializers.ValidationError("Message is not valid.")
        return encrypted_messages

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
        keypair = KeyPair.objects.get(id=validated_data.get("keypair_id"))
        passphrase = get_passphrase(validated_data.get("passphrase"), keypair)
        private_key_pem = keypair.private_key.encode("utf-8")

        decrypted_message = decrypt_message(
            validated_data.get("message"), private_key_pem, passphrase
        )
        if not decrypted_message:
            raise serializers.ValidationError(
                {"error": ["Decryption failed: Invalid keypair selected."]}
            )
        return {"message": decrypted_message.decode()}
