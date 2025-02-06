import requests
from rest_framework import serializers
from django.contrib.auth.models import User
from main.utils import generate_passphrase, hash_passphrase


class UserSignUpSerializer(serializers.Serializer):
    pass_phrase = serializers.CharField(read_only=True)

    def create(self, validated_data):
        passphrase = generate_passphrase()
        hashed_passphrase = hash_passphrase(passphrase)
        while User.objects.filter(username=passphrase).exists():
            passphrase = generate_passphrase()
            hashed_passphrase = hash_passphrase(passphrase)
        url = "https://apiresonance.neuronus.net/api/user/register"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"seed": passphrase}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            address = None
            if response_data.get("success") == True:
                url = "https://apiresonance.neuronus.net/api/user/login"
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    response_data = response.json()
                    address = response_data.get("identity", {}).get("address", None)
                user = User.objects.create(username=passphrase)
                user.set_password(hashed_passphrase)
                user.save()
                user.profile.address = address
                user.profile.save()
        except Exception as e:
            print(f"Error: {e}")
            raise serializers.ValidationError(
                {"error": "Failed to create passphrase please refresh page"}
            )
        return {"pass_phrase": passphrase}
