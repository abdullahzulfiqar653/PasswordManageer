from rest_framework import generics
from rest_framework.permissions import AllowAny
from api.serializers import UserSignUpSerializer


class UserSignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignUpSerializer