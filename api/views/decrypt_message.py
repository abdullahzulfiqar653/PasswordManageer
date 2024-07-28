from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.serializers.decrypt_message import DecryptMessageSerializer


class DecryptMessageView(generics.CreateAPIView):
    serializer_class = DecryptMessageSerializer
    permission_classes = [IsAuthenticated]
