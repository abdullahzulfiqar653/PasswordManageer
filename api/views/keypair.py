from rest_framework import generics, permissions, filters
from api.models.keypair import KeyPair
from rest_framework.permissions import AllowAny
from api.serializers.keypair import KeyPairSerializer, MainKeyPairSerializer


class KeyPairListCreateView(generics.ListCreateAPIView):
    serializer_class = KeyPairSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter KeyPairs by the current authenticated user
        return KeyPair.objects.filter(user=self.request.user)


class KeyPairRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = KeyPairSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter Keypairs by the current authenticated user
        return KeyPair.objects.filter(user=self.request.user)


class MainKeyPairCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = MainKeyPairSerializer
