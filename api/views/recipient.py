from rest_framework import generics, permissions, filters
from api.models.recipient import Recipient
from api.serializers.recipient import RecipientSerializer


class RecipientListCreateView(generics.ListCreateAPIView):
    serializer_class = RecipientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter KeyPairs by the current authenticated user
        return Recipient.objects.filter(user=self.request.user)


class RecipientRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter Recipients by the current authenticated user
        return Recipient.objects.filter(user=self.request.user)
