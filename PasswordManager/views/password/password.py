from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from PasswordManager.serializers.password import PasswordSerializer


class PasswordListCreateView(generics.ListCreateAPIView):
    serializer_class = PasswordSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "username", "url", "notes", "emoji"]
    filterset_fields = ["folder"]

    def get_queryset(self):
        return self.request.user.passwords.all().order_by("-created_at")


class PasswordRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PasswordSerializer

    def get_queryset(self):
        return self.request.user.passwords.all()
