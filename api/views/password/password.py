from rest_framework import generics
from rest_framework import permissions
from api.models.password import Password
from api.serializers.password import PasswordCreateSerializer


class PasswordListCreateView(generics.ListCreateAPIView):
    serializer_class = PasswordCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter passwords by the current authenticated user
        return Password.objects.filter(user=self.request.user)


class PasswordRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PasswordCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter passwords by the current authenticated user
        return Password.objects.filter(user=self.request.user)
