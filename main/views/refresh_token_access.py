from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from main.serializers import RefreshTokenSerializer


class RefreshTokenAPIView(generics.RetrieveAPIView):
    """
    - If you are logged in successfully, the refresh token is stored in an HTTP-only cookie.
    - To obtain a new access token, send a **GET request** to this endpoint.
    - The access token will be returned in the response.
    """

    permission_classes = []
    serializer_class = RefreshTokenSerializer

    def retrieve(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("neuro_refresh_token")

        if not refresh_token:
            raise AuthenticationFailed(detail="No refresh token found in cookies")

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({"access": access_token})
        except Exception:
            raise AuthenticationFailed(detail="Invalid refresh token")
