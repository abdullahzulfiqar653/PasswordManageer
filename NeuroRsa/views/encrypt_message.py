from rest_framework import generics
from NeuroRsa.serializers.encrypt_message import EncryptMessageSerializer


class EncryptMessageView(generics.CreateAPIView):
    serializer_class = EncryptMessageSerializer
