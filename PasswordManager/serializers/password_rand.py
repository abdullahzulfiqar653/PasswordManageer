import random
import string
from rest_framework import serializers


class RandomPasswordCreateSerializer(serializers.Serializer):
    password = serializers.CharField(read_only=True)
    length = serializers.IntegerField(write_only=True)
    is_alphabets = serializers.BooleanField(write_only=True, default=False)
    is_lowercase = serializers.BooleanField(write_only=True, default=False)
    is_uppercase = serializers.BooleanField(write_only=True, default=False)
    is_numeric = serializers.BooleanField(write_only=True, default=False)
    is_special = serializers.BooleanField(write_only=True, default=False)

    def validate(self, data):
        if not any(
            [
                data["is_alphabets"],
                data["is_lowercase"],
                data["is_uppercase"],
                data["is_numeric"],
                data["is_special"],
            ]
        ):
            raise serializers.ValidationError(
                "At least one character type must be selected."
            )

        return data

    def validate_length(self, length):
        if length < 10:
            raise serializers.ValidationError("length must be 10 or greater")
        return length

    def create(self, validated_data):
        character_sets = []

        if validated_data.get("is_alphabets"):
            character_sets.append(string.ascii_letters)
        if validated_data.get("is_lowercase"):
            character_sets.append(string.ascii_lowercase)
        if validated_data.get("is_uppercase"):
            character_sets.append(string.ascii_uppercase)
        if validated_data.get("is_numeric"):
            character_sets.append(string.digits)
        if validated_data.get("is_special"):
            character_sets.append(string.punctuation)

        if not character_sets:
            raise serializers.ValidationError("No valid character sets selected.")

        random_password = "".join(
            random.choice("".join(character_sets))
            for _ in range(validated_data["length"])
        )

        return {"password": random_password}
