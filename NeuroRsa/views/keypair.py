from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from NeuroRsa.serializers.keypair import KeyPairSerializer, MainKeyPairSerializer


class KeyPairListCreateView(generics.ListCreateAPIView):
    serializer_class = KeyPairSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        return self.request.user.keypairs.all()


class KeyPairRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = KeyPairSerializer

    def get_queryset(self):
        return self.request.user.keypairs.all()


class MainKeyPairCreateView(generics.CreateAPIView):
    serializer_class = MainKeyPairSerializer
    permission_classes = [AllowAny]
