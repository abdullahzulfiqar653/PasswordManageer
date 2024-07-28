from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.serializers.encrypt_message import EncryptMessageSerializer


class EncryptMessageView(generics.CreateAPIView):
    serializer_class = EncryptMessageSerializer
    permission_classes = [IsAuthenticated]
