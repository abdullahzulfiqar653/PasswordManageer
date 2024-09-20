from rest_framework import generics
from rest_framework.permissions import AllowAny
from main.serializers import UserSignInSerializer


class UserSignInView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignInSerializer
