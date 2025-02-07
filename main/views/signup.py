from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from main.serializers import UserSignUpSerializer


class UserSignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignUpSerializer
    
    @swagger_auto_schema(
        operation_description="User **sign-up** endpoint. Accepts user details to create a new user account.",
        request_body=UserSignUpSerializer,
        responses={
            201: 'User created successfully.',
            400: 'Bad request. Invalid data provided.',
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
