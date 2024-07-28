from rest_framework import generics, permissions, filters
from api.models.recipient import Recipient
from api.serializers.recipient import RecipientSerializer


class RecipientListCreateView(generics.ListCreateAPIView):
    serializer_class = RecipientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter KeyPairs by the current authenticated user
        return Recipient.objects.filter(user=self.request.user)


# class PasswordRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = PasswordCreateSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         # Filter passwords by the current authenticated user
#         return Password.objects.filter(user=self.request.user)
