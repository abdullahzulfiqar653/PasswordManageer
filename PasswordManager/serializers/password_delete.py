from rest_framework import serializers

from PasswordManager.models.password import Password


class PasswordDeleteSerializer(serializers.Serializer):
    passwords = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Password.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        """
        Modifying the queryset of the passwords field based on the request user.
        """
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if hasattr(request, "user") and request.user.is_authenticated:
            self.fields["passwords"].queryset = request.user.passwords.all()

    def delete_passwords(self):
        password_ids = [password.id for password in self.validated_data["passwords"]]
        Password.objects.filter(id__in=password_ids).delete()
