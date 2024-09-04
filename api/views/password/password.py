from rest_framework import generics, filters
from api.serializers.password import PasswordSerializer


class PasswordListCreateView(generics.ListCreateAPIView):
    serializer_class = PasswordSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "username", "url", "notes", "emoji"]

    def get_queryset(self):
        return self.request.user.passwords.all()


class PasswordRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PasswordSerializer

    def get_queryset(self):
        return self.request.user.passwords.all()
