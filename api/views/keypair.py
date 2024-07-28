from rest_framework import generics, permissions, filters
from api.models.keypair import KeyPair
from api.serializers.keypair import KeyPairSerializer


class KeyPairListCreateView(generics.ListCreateAPIView):
    serializer_class = KeyPairSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ["title", "username", "url", "notes", "emoji"]

    def get_queryset(self):
        # Filter KeyPairs by the current authenticated user
        return KeyPair.objects.filter(user=self.request.user)


# class PasswordRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = PasswordCreateSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         # Filter passwords by the current authenticated user
#         return Password.objects.filter(user=self.request.user)
