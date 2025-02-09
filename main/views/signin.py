from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from main.serializers import UserSignInSerializer


class UserSignInView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignInSerializer

    @swagger_auto_schema(
        operation_description="""
        **User Sign-In Endpoint**  

        - Accepts only a `pass-phrase` for authentication.  
        - Generates and returns an authentication **token**.  
        """,
        request_body=UserSignInSerializer,
        responses={
            200: "Sign-in successful. Returns authentication token.",
            400: "Bad request. Invalid seed provided.",
            401: "Unauthorized. Invalid credentials.",
        },
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.pop("refresh", None)
        if refresh_token:
            response.set_cookie(
                "neuro_refresh_token", refresh_token, httponly=True, secure=True
            )
        return response
