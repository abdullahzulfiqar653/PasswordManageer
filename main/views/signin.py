from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from main.serializers import UserSignInSerializer


class UserSignInView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignInSerializer
    
    @swagger_auto_schema(
        operation_description="User **sign-in** endpoint. Accepts a **username** and **password** to authenticate a user.",
        request_body=UserSignInSerializer,
        responses={
            200: 'Sign-in successful. Returns the user details and authentication token.',
            400: 'Bad request. Invalid username or password.',
            401: 'Unauthorized. Invalid credentials.',
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
