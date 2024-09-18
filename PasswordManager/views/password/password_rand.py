from rest_framework import generics
from rest_framework import permissions
from PasswordManager.serializers import RandomPasswordCreateSerializer


class RandomPasswordCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RandomPasswordCreateSerializer
